import math
# import urlib
from settings import Station17Positions


class Grid:
    # Parameterized Constructor
    def __init__(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.ref_pose_1 = ref_pose_1
        self.ref_pose_2 = ref_pose_2
        self.ref_pose_3 = ref_pose_3
        self.rows = rows
        self.columns = columns
        self.get_ref_x_y_dist()
        self.get_ref_x_y_z_dist()
        self.items={} #self.initItems(rows,columns)
        self.iterator=0 
               
    def initItems(self,r,c):
        rows=[]
        for i in range(r*c):           
            rows.append(False)
        return rows

    def get_ref_x_y_dist(self):
        self.ref_x = self.ref_pose_1[0]
        self.ref_y = self.ref_pose_1[1]
        self.x_dist = self.ref_pose_2[0] - self.ref_pose_1[0]
        self.y_dist = self.ref_pose_3[1] - self.ref_pose_1[1]

    def get_ref_x_y_z_dist(self):
        self.ref_x = self.ref_pose_1[0]
        self.ref_y = self.ref_pose_1[1]
        self.ref_z = self.ref_pose_1[2]
        self.x_dist = self.ref_pose_2[0] - self.ref_pose_1[0]
        self.y_dist = self.ref_pose_3[1] - self.ref_pose_1[1]
        self.z_dist = self.ref_pose_3[2] - self.ref_pose_1[2]

    def get_x_y_in_grid(self, location):
        y_in_grid = math.ceil(location / self.columns) - 1
        x_in_grid = (location-1) - (y_in_grid * self.columns)
        return x_in_grid, y_in_grid
    
    def get_x_y_z_in_grid(self, location):
        y_in_grid = math.ceil(location / self.columns) - 1
        x_in_grid = (location-1) - (y_in_grid * self.columns)
        z_in_grid = math.ceil(location / self.columns) - 1
        return x_in_grid, y_in_grid, z_in_grid

    def get_target_x_y(self, location):
        x_in_grid, y_in_grid = self.get_x_y_in_grid(location)
        x_target = self.ref_x + (self.x_dist * x_in_grid)
        y_target = self.ref_y + (self.y_dist * y_in_grid)
        pose_to_sent = [x_target, y_target, self.ref_pose_1[2], self.ref_pose_1[3], self.ref_pose_1[4], self.ref_pose_1[5]]
        return pose_to_sent

    def get_target_x_y_z(self, location):
        x_in_grid, y_in_grid, z_in_grid = self.get_x_y_z_in_grid(location)
        x_target = self.ref_x + (self.x_dist * x_in_grid)
        y_target = self.ref_y + (self.y_dist * y_in_grid)
        z_target = self.ref_z + (self.z_dist * z_in_grid)
        pose_to_sent = [x_target, y_target, z_target, self.ref_pose_1[3], self.ref_pose_1[4], self.ref_pose_1[5]]
        return pose_to_sent

    def get_target_x_y_list(self, location):
        x_in_grid, y_in_grid = self.get_x_y_in_grid(location)        
        x_target = self.ref_x + (self.x_dist * x_in_grid)
        y_target = self.ref_y + (self.y_dist * y_in_grid)        
        return x_target, y_target


class GridInevitable:
    # Parameterized Constructor
    def __init__(self, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns):
        self.ref_pose_1 = ref_pose_1
        self.ref_pose_2 = ref_pose_2
        self.ref_pose_3 = ref_pose_3
        self.rows = rows
        self.columns = columns
        self.get_ref_x_y_dist()
        self.items={} #self.initItems(rows,columns)
        self.iterator=0 
               
    def initItems(self,r,c):
        rows=[]
        for i in range(r*c):           
            rows.append(False)
        return rows

    def get_ref_x_y_dist(self):
        self.ref_x = self.ref_pose_1[0]
        self.ref_y = self.ref_pose_1[1]
        self.x_dist = (self.ref_pose_2[0] - self.ref_pose_1[0]) / (self.columns-1) # Negative direction
        self.y_dist = (self.ref_pose_3[1] - self.ref_pose_1[1]) / (self.rows-1)

    def get_x_y_in_grid(self, location):
        y_in_grid = math.ceil(location / self.columns) - 1
        x_in_grid = (location-1) - (y_in_grid * self.columns)
        return x_in_grid, y_in_grid
    
    def get_target_x_y(self, location):
        x_in_grid, y_in_grid = self.get_x_y_in_grid(location)
        x_target = self.ref_x + (self.x_dist * x_in_grid)
        y_target = self.ref_y + (self.y_dist * y_in_grid)
        pose_to_sent = [x_target, y_target, self.ref_pose_1[2], self.ref_pose_1[3], self.ref_pose_1[4], self.ref_pose_1[5]]
        return pose_to_sent

    def get_target_x_y_list(self, location):
        x_in_grid, y_in_grid = self.get_x_y_in_grid(location)        
        x_target = self.ref_x + (self.x_dist * x_in_grid)
        y_target = self.ref_y + (self.y_dist * y_in_grid)        
        return x_target, y_target


class GridBatch:
    # Parameterized Constructor
    def __init__(self, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns):
        self.ref_pose_1 = ref_pose_1
        self.ref_pose_2 = ref_pose_2
        self.ref_pose_3 = ref_pose_3
        self.ref_pos_4 = ref_pose_4
        self.ref_pos_5 = ref_pose_5
        self.p_rows = p_rows
        self.p_columns = p_columns
        self.ch_rows = ch_rows
        self.ch_columns = ch_columns  
        self.parent_grid = Grid(ref_pose_1, ref_pose_2, ref_pose_3, self.p_rows , self.p_columns)
        self.child_grid = Grid(ref_pose_1, ref_pose_4, ref_pose_5, self.ch_rows , self.ch_columns)
        self.iterator=0
        self.items={} #self.initItems(p_rows, p_columns,ch_rows, ch_columns)
        
    def initItems(self, pr, pc, cr, cc):
        rows=[]
        for i in range(pr*pc*cr*cc):           
            rows.append(False)
        return rows

    def get_target_x_y(self , parent_grid_location, child_grid_location):
        x_parent_grid, y_parent_grid = self.parent_grid.get_x_y_in_grid(parent_grid_location)
        x_child_grid, y_child_grid = self.child_grid.get_x_y_in_grid(child_grid_location)

        x_parent = self.parent_grid.ref_x + (self.parent_grid.x_dist * x_parent_grid)
        y_parent = self.parent_grid.ref_y + (self.parent_grid.y_dist * y_parent_grid)

        x_child = (self.child_grid.x_dist * x_child_grid)
        y_child =  (self.child_grid.y_dist * y_child_grid)

        x_sent = x_parent + x_child
        y_sent = y_parent + y_child

        pose_to_sent = [x_sent , y_sent, self.ref_pose_1[2], self.ref_pose_1[3], self.ref_pose_1[4], self.ref_pose_1[5]]
        return pose_to_sent


class GridCoagulation:
    # Parameterized Constructor
    def __init__(self, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8):
        self.id = id
        self.ref_pose_1=ref_pose_1
        self.ref_pose_2=ref_pose_2
        self.ref_pose_3=ref_pose_3
        self.ref_pose_4=ref_pose_4
        self.ref_pose_5=ref_pose_5
        self.ref_pose_6=ref_pose_6
        self.ref_pose_7=ref_pose_7
        self.ref_pose_8=ref_pose_8
        
    def get_radius(self):
        return math.dist((self.ref_pose_1[0], self.ref_pose_1[1]), (self.ref_pose_2[0], self.ref_pose_2[1])) / 2

    def get_center_pose(self):
        x_center = self.ref_pose_1[0] + ((self.ref_pose_2[0] - self.ref_pose_1[0]) / 2)
        # y_center = self.ref_pose_1[1] + ((self.ref_pose_2[1] - self.ref_pose_1[1]) / 2)
        return [x_center, self.ref_pose_2[1], self.ref_pose_1[2], self.ref_pose_1[3], self.ref_pose_1[4], self.ref_pose_1[5]] 

    def get_x_y_circle(self, tube_location):
        theta = math.radians((tube_location-1) * self.angle)
        x = self.center_pose[0] + (self.radius * math.cos(theta))
        y = self.center_pose[1] + (self.radius * math.sin(theta))
        return x, y #, math.degrees(theta)

    def get_pose_circle(self, tube_location):       
        match tube_location:
            case 1:
                return self.ref_pose_1
            case 2:
                return self.ref_pose_2
            case 4:
                return self.ref_pose_3
            case 6:
                return self.ref_pose_4
            case 7:
                return self.ref_pose_5
            case 8:
                return self.ref_pose_6
            case 9:
                return self.ref_pose_7
            case 10:
                return self.ref_pose_8


def testGridCoagulation():
    g = GridCoagulation({'x':0.2621,'y':0.152,'z':-0.055,'rx':120,'ry':150,'rz':150}, {'x':0.521,'y':0.162,'z':-0.055,'rx':120,'ry':150,'rz':150}, 10)
    
    x_arr = []
    y_arr = []

    for i in range(10):
        print(i+1)
        x, y = g.get_x_y_circle(i+1)
        x_arr.append(x)
        y_arr.append(y)
        print(x, y)
        print("----------------")

    
    
# testGridCoagulation()


def testGrid():
    ref1 = [200,-100,0,0,0,0]
    ref2 = [20,-100,0,0,0,0]
    ref3 = [200,-50,0,0,0,0]

    g = GridInevitable([200,-100,0,0,0,0], 
    [20,-100,0,0,0,0],
    [200,-50,0,0,0,0], 4, 10)
    rows = 5
    columns=10
    for j in range(10):
        newx = ref1[0] - (((ref1[0]-ref2[0])/(columns-1))) * j
        for i in range(5):
            if not i == 2:
                newy = ref1[1] + (((ref3[1]-ref1[1])/(rows-1))) * i     
                print(newx,newy)
    # for i in range(50):
    #     # for i in range(4):
    #         print(i+1)
    #         tubeLocation=g.get_target_x_y(i+1)
    #         r=[tubeLocation[0], tubeLocation[1], tubeLocation[2], tubeLocation[3], tubeLocation[4], tubeLocation[5]]
    #         print(r)
    #         print("----------------")
    
# testGrid()


def testGridBatch():
    g = GridBatch({'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':200,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':300,'z':120,'rx':120,'ry':150,'rz':150},1,2,{'x':110,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':115,'z':120,'rx':120,'ry':150,'rz':150},2,5)
    for i in range(2):
        for j in range(10):
            print(i+1, j+1)
            r = g.get_target_x_y(i+1,j+1)
            print(r)
            print("----------------")

#testGridBatch()

def testGridBatchHae():
    g = GridBatch({'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':200,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},1,2,{'x':110,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
            {'x':100,'y':115,'z':120,'rx':120,'ry':150,'rz':150},2,5)
    for i in range(2):
        for j in range(10):
            print(i+1, j+1)
            r = g.get_target_x_y(i+1,j+1)
            print(r)
            print("----------------")

#testGridBatchHae()