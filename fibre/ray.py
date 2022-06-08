import numpy as np
import numpy.random
#import matplotlib.pyplot as plt
import shapely
from shapely.geometry import Polygon, LineString, LinearRing, Point, MultiLineString
from shapely.geometry.collection import GeometryCollection
#from descartes import PolygonPatch
from itertools import tee
from fibre.optics import snell, R, T

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def angle_to_line(angle):
    unit_vector = np.array([np.cos(angle), np.sin(angle)])
    unit_line = LineString([np.zeros(2), unit_vector])
    return unit_line

def line_to_angle(line):
    coord1 = line.coords[0]
    coord2 = line.coords[1]
    x = coord2[0]-coord1[0]
    y = coord2[1]-coord1[1]
    angle = np.arctan2(y,x)
    return angle

def get_normal(obj, intersection, plot_line, interior=False):
    side = 0
    min_distance = np.inf
    intersection_side = None
    for p0, p1 in pairwise(obj.exterior.coords):
        line = LineString( [p0,p1])
        ring = LinearRing( [p0,p1, intersection])
        poly = Polygon(ring)
        distance = poly.area/line.length
        if distance < min_distance:
            min_distance = distance
            intersection_side = side
        side += 1
    points = obj.exterior.coords[intersection_side:intersection_side+2]
    seg_vec = np.array(points[1])-np.array(points[0])
    seg_vec = seg_vec/np.linalg.norm(seg_vec)
    line = LineString([np.zeros(2), seg_vec])

    exterior_line = shapely.affinity.rotate(line, -90., origin=(0.,0.))
    interior_line = shapely.affinity.rotate(line, 90., origin=(0.,0.))
    if False:
        exterior_line_trans = shapely.affinity.translate(exterior_line, xoff=x0, yoff=y0)
        x, y = exterior_line_trans.xy
        #plt.plot(x, y, color='tab:green', linewidth=2, solid_capstyle='round', zorder=1, ls='--')

        interior_line_trans = shapely.affinity.translate(interior_line, xoff=x0, yoff=y0)
        x, y = interior_line_trans.xy
        #plt.plot(x, y, color='tab:red', linewidth=2, solid_capstyle='round', zorder=1, ls='--')
    return (np.array(list(interior_line.coords)[1]), np.array(list(exterior_line.coords)[1]))

def global_to_local(x_axis, angle):
    return np.angle(np.exp(1j*(angle-x_axis)))

def local_to_global(x_axis, angle):
    return np.angle(np.exp(1j*(x_axis+angle)))

def get_angle_to_norm(norm_vector, angle, print_output=False):
    norm_angle = np.arctan2(norm_vector[1],norm_vector[0])
    local_inc_angle_left1 = global_to_local(norm_angle, angle)
    local_inc_angle_left2 = global_to_local(norm_angle, -angle)
    local_inc_angle_left = local_inc_angle_left1

    rot_angle = np.angle(np.exp(1j*(angle-np.pi)))
    local_inc_angle_right1 = global_to_local(norm_angle, rot_angle)
    local_inc_angle_right2 = global_to_local(norm_angle, -rot_angle)

    local_inc_angle_right = local_inc_angle_right1

    if np.abs(local_inc_angle_right) < np.abs(local_inc_angle_left):
        angle_to_norm = local_inc_angle_right
    else:
        angle_to_norm = local_inc_angle_left
    return norm_angle, angle_to_norm

class Ray():

    def __init__(self, origin, end_point, ref_index=1.0, intensity=1.0, color='gray'):
        self.origin = origin
        self.ref_index = ref_index
        self.end_point = end_point
        self.color = color
        self.intensity = intensity

    @property
    def prop_angle(self):
        x = self.end_point[0]-self.origin[0]
        y = self.end_point[1]-self.origin[1]
        angle = np.arctan2(y,x)
        return angle

    def propagate(self, distance, angle):
        end_point_x = distance*np.cos(angle) + self.origin[0]
        end_point_y = distance*np.sin(angle) + self.origin[1]
        end_point = np.array([end_point_x, end_point_y])
        self.end_point = end_point

    def back_propagate(self, distance, angle):
        end_point_x = -distance*np.cos(angle) + self.origin[0]
        end_point_y = -distance*np.sin(angle) + self.origin[1]
        end_point = np.array([end_point_x, end_point_y])
        self.end_point = end_point

    def reverse(self):
        tmp = np.copy(self.origin)
        self.origin = np.copy(self.end_point)
        self.end_point = tmp

    def plot(self, ax):
        line = self.get_line()
        x, y = line.xy
        ax.plot(x, y, color=self.color, linewidth=3, solid_capstyle='round', zorder=1,
                alpha=self.intensity)

    def get_line(self):
        return LineString([self.origin, self.end_point])

    def __repr__(self):
        return "{}, {}, {}".format(self.origin, self.end_point, np.degrees(self.prop_angle))

class RaySimulation():

    def __init__(self):
        self.rays = []
        self.finished_rays = []
        self.objects = []
        self.ref_index = []
        self.transmission = 0.

    def init_ray(self, prop_angle):
        origin = -0.5*np.array([np.cos(prop_angle), np.sin(prop_angle)]) + np.array([0., 0.1])
        #origin = np.array([0., 0.2]) +
        ray = Ray(origin, origin)
        ray.propagate(1.0, prop_angle)
        self.rays.append(ray)

    def create_core(self, radius, length):
        polygon = Polygon([(-radius, 0.1-length), (radius, 0.1-length), (radius, 0.1), (-radius, 0.1)])
        self.objects.append(polygon)
        self.ref_index.append(1.5)

    def create_prism(self, left, right, height, angle):
        polygon = Polygon([(left, -height), (right, -height),
                           (right-np.tan(np.radians(angle))*height*2., height), (left, height)])
        polygon = shapely.geometry.polygon.orient(polygon)
        self.objects.append(polygon)
        self.ref_index.append(1.5)

    def init_background(self):
        self.create_core(0.4, 20.)
        #self.create_prism(0.1, 5.1, 0.5, 30.)

    def add_cladding(self, inner_radius, outer_radius, length):
        poly_points = []
        poly_points.append((inner_radius, 0.1-length))
        poly_points.append((outer_radius, 0.1-length))
        poly_points.append((outer_radius, 0.1))
        poly_points.append((inner_radius, 0.1))

        polygon = shapely.geometry.polygon.orient(Polygon(poly_points))
        self.objects.append(polygon)
        self.ref_index.append(1.48)

        poly_points = []
        poly_points.append((-outer_radius, 0.1-length))
        poly_points.append((-inner_radius, 0.1-length))
        poly_points.append((-inner_radius, 0.1))
        poly_points.append((-outer_radius, 0.1))

        polygon = shapely.geometry.polygon.orient(Polygon(poly_points))
        self.objects.append(polygon)
        self.ref_index.append(1.48)

    def add_oil(self, inner_radius, outer_radius, length, height, period):
        poly_points = []
        poly_points.append((inner_radius, 0.1-length))
        noise_level = 0.01
        for y in np.linspace(0.1, 0.1-length, 200)[::-1]:
            x = np.random.normal(0, noise_level, 1) + height*np.sin(2*np.pi*y/period) +outer_radius
            poly_points.append((x, y))
        poly_points.append((inner_radius, 0.1))
        #poly_points.append((0.1,0.5))
        polygon = shapely.geometry.polygon.orient(Polygon(poly_points))
        self.objects.append(polygon)
        self.ref_index.append(1.5)

        poly_points = []
        poly_points.append((-inner_radius, 0.1-length))
        poly_points.append((-inner_radius, 0.1))
        for y in np.linspace(0.1, 0.1-length, 200):
            x = np.random.normal(0, noise_level, 1) -height*np.sin(2*np.pi*y/period)-outer_radius
            poly_points.append((x, y))

        #poly_points.append((0.1,0.5))
        polygon = shapely.geometry.polygon.orient(Polygon(poly_points))
        self.objects.append(polygon)
        self.ref_index.append(1.5)


    def plot_objects(self, ax):
        for obj in self.objects:
            patch = PolygonPatch(obj, ec='k', fill=False)
            ax.add_patch(patch)

    def plot_rays(self, ax):
        for iray, ray in enumerate(self.finished_rays):
            ray.plot(ax)

    def find_intersection(self, obj, ray):
        inter = obj.intersection(ray)
        if isinstance(inter, MultiLineString) or isinstance(inter, GeometryCollection):
            inter = inter[0]
        first_inter = np.array(inter.coords)
        return first_inter

    def find_container(self, coords):
        point = Point(coords)
        for iobj, obj in enumerate(self.objects):
            if obj.contains(point):
                return iobj
        return None

    def main(self):
        #print("############################")
        self.transmission = 0.
        for steps in range(1):
            iray = 0
            while len(self.rays) > 0:
                ray = self.rays[0]
                if ray.intensity < 0.01:
                    #print("{} removed due to ray intensity".format(iray))
                    self.rays.remove(ray)
                    self.finished_rays.append(ray)
                    continue

                iray += 1
                if iray> 100:
                    break
                closest_intersection = np.inf
                intersection_object = None
                intersection_iobj = None
                intersection_point = None
                intersection_side = None
                for iobj, obj in enumerate(self.objects):
                    line = ray.get_line()
                    if line.intersects(obj) and not line.touches(obj):
                        intersections = self.find_intersection(obj, line)
                        #print("intersections: {}".format(intersections))
                        for i_inter in range(intersections.shape[0]):
                            intersection = intersections[i_inter, :]
                            if np.all(np.isclose(i_inter, ray.origin)):
                                continue

                            tmp_ray = Ray(ray.origin, intersection)
                            tmp_line = tmp_ray.get_line()
                            dist_to_intersection = tmp_line.length
                            #print("intersection: {}, dist: {}".format(intersection, dist_to_intersection))
                            if dist_to_intersection < closest_intersection and dist_to_intersection > 1e-10:
                                closest_intersection = dist_to_intersection
                                intersection_object = obj
                                intersection_iobj = iobj
                                intersection_point = intersection

                #print("intersection iobject: {}".format(iobj))
                #print("intersection point: {}".format(intersection_point))
                obj = intersection_object
                iobj = intersection_iobj
                if obj is None:
                    self.rays.remove(ray)
                    self.finished_rays.append(ray)
                    continue
                line = ray.get_line()
                #if line.intersects(obj) and not line.touches(obj):
                if True:
                    #print("valid intersection object")
                    """
                    intersections = self.find_intersection(obj, line)
                    #print("intersections: {}".format(intersections))
                    if np.all(np.isclose(intersections[0,:], ray.origin)):
                        if intersections.shape[0] == 1:
                            continue
                        else:
                            intersection = intersections[1,:]
                    else:
                        intersection = intersections[0,:]
                    """
                    intersection = intersection_point
                    ray.end_point = intersection
                    #print("intersection: {}".format(intersection))
                    #print("ray: {}".format(ray))
                    if np.all(np.isclose(intersection, ray.origin)):
                        continue

                    normals = get_normal(obj, intersection, False)

                    norm_angle_int, local_angle_to_int_norm = get_angle_to_norm(normals[0],
                                                                                ray.prop_angle,
                                                                                print_output=False)
                    norm_angle_ext, local_angle_to_ext_norm = get_angle_to_norm(normals[1],
                                                                                ray.prop_angle,
                                                                                print_output=False)
                    no_reflection = False
                    if np.isclose(norm_angle_ext, np.radians(-90)):
                        #print("turn of reflection for ray: {}".format(ray))
                        no_reflection = True

                    inside_point = intersection + normals[0]*1e-2
                    outside_point = intersection + normals[1]*1e-2

                    line_to_outside = LineString((ray.origin, outside_point))
                    line_to_inside = LineString((ray.origin, inside_point))

                    if line_to_outside.length < line_to_inside.length:
                        local_angle = local_angle_to_ext_norm
                        normal_angle = norm_angle_ext
                        conj_normal_angle = norm_angle_int
                    else:
                        local_angle = local_angle_to_int_norm
                        normal_angle = norm_angle_int
                        conj_normal_angle = norm_angle_ext



                    refl_angle = -local_angle
                    refl_angle_global = local_to_global(normal_angle, refl_angle)

                    outside_obj = self.find_container(outside_point)
                    inside_obj = self.find_container(inside_point)

                    line = ray.get_line()
                    if obj.contains(line.centroid):
                        is_inside = True
                    else:
                        is_inside = False


                    if outside_obj is None:
                        outside_n = 1.0
                    else:
                        outside_n = self.ref_index[outside_obj]

                    if inside_obj is None:
                        inside_n = 1.0
                    else:
                        inside_n = self.ref_index[inside_obj]

                    if is_inside:
                        n2 = outside_n
                        n1 = inside_n
                    else:
                        n1 = outside_n
                        n2 = inside_n

                    if outside_n == 1.0:
                        dist = 21.
                    else:
                        dist = 21*np.sqrt(2.)

                    if no_reflection is False:
                        refl_intensity = R(n1, local_angle, n2)
                        refl = Ray(intersection, intersection, color='tab:red', intensity=refl_intensity*ray.intensity)
                        refl.propagate(dist, refl_angle_global)

                    local_trans_angle = snell(n1, local_angle, n2)
                    trans_intensity = T(n1, local_angle, n2)
                    global_trans_angle = local_to_global(conj_normal_angle, local_trans_angle)



                    trans = Ray(intersection, intersection, color='tab:green', intensity=trans_intensity*ray.intensity)

                    trans.propagate(dist, global_trans_angle)
                    if no_reflection is False:
                        self.rays.append(refl)
                    else:
                        #print("adding ray {} to transmission: {}".format(iray, ray.intensity*trans_intensity))
                        if iobj == 0:
                            self.transmission += ray.intensity*trans_intensity
                    self.rays.append(trans)
                self.rays.remove(ray)
                self.finished_rays.append(ray)
