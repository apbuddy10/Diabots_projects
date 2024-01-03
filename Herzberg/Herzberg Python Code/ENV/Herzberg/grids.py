import math
import urlib


class Grid:
    # Parameterized Constructor
    def __init__(self, id, ref_pose_1, ref_pose_2, ref_pose_3, rows, columns): 
        assert type(ref_pose_1) is dict
        assert type(ref_pose_2) is dict
        assert type(ref_pose_3) is dict
        self.id = id
        self.ref_pose_1 = urlib.poseToList(ref_pose_1) 
        self.ref_pose_2 = urlib.poseToList(ref_pose_2)
        self.ref_pose_3 = urlib.poseToList(ref_pose_3)
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
        self.x_dist = self.ref_pose_2[0] - self.ref_pose_1[0]
        self.y_dist = self.ref_pose_3[1] - self.ref_pose_1[1]

    def get_x_y_in_grid(self, location):
        y_in_grid = math.ceil(location / self.columns) - 1
        x_in_grid = (location-1) - (y_in_grid * self.columns)
        return x_in_grid, y_in_grid

    def get_target_x_y(self, location):
        x_in_grid, y_in_grid = self.get_x_y_in_grid(location)
        x_target = self.ref_x + (self.x_dist * x_in_grid)
        y_target = self.ref_y + (self.y_dist * y_in_grid)
        pose_to_sent = [x_target, y_target, self.ref_pose_1[2], self.ref_pose_1[3], self.ref_pose_1[4], self.ref_pose_1[5]]
        return urlib.listToPose(pose_to_sent)

    def get_target_x_y_list(self, location):
        x_in_grid, y_in_grid = self.get_x_y_in_grid(location)        
        x_target = self.ref_x + (self.x_dist * x_in_grid)
        y_target = self.ref_y + (self.y_dist * y_in_grid)        
        return x_target, y_target


class GridBatch:
    # Parameterized Constructor
    def __init__(self, id, ref_pose_1, ref_pose_2, ref_pose_3, p_rows, p_columns, ref_pose_4, ref_pose_5, ch_rows, ch_columns):
        assert type(ref_pose_1) is dict
        assert type(ref_pose_2) is dict
        assert type(ref_pose_3) is dict
        assert type(ref_pose_4) is dict
        assert type(ref_pose_5) is dict
        self.id = id
        self.ref_pose_1 = urlib.poseToList(ref_pose_1) 
        self.ref_pose_2 = urlib.poseToList(ref_pose_2)
        self.ref_pose_3 = urlib.poseToList(ref_pose_3)
        self.ref_pos_4 = urlib.poseToList(ref_pose_4)
        self.ref_pos_5 = urlib.poseToList(ref_pose_5)
        self.p_rows = p_rows
        self.p_columns = p_columns
        self.ch_rows = ch_rows
        self.ch_columns = ch_columns  
        self.parent_grid = Grid(self.id, ref_pose_1, ref_pose_2, ref_pose_3, self.p_rows , self.p_columns)
        self.child_grid = Grid(self.id, ref_pose_1, ref_pose_4, ref_pose_5, self.ch_rows , self.ch_columns)
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
        return urlib.listToPose(pose_to_sent)


class GridChemistry:
    # Parameterized Constructor
    def __init__(self, id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5, ref_pose_6):
        assert type(ref_pose_1) is dict
        assert type(ref_pose_2) is dict
        assert type(ref_pose_3) is dict
        assert type(ref_pose_4) is dict
        assert type(ref_pose_5) is dict
        assert type(ref_pose_6) is dict
        self.id = id
        self.ref_pose_1 = urlib.poseToList(ref_pose_1) 
        self.ref_pose_2 = urlib.poseToList(ref_pose_2)
        self.ref_pose_3 = urlib.poseToList(ref_pose_3)
        self.ref_pose_4 = urlib.poseToList(ref_pose_4)
        self.ref_pose_5 = urlib.poseToList(ref_pose_5)
        self.ref_pose_6 = urlib.poseToList(ref_pose_6)

        '''self.ref_pose_1 = [-0.03854,0.06507,0.21,3.141,-0.016,0]
        self.ref_pose_2 = [0.13164,0.066,0.21,3.141,0.005,0]
        self.ref_pose_3 = [-0.0566,0.107,0.21,2.985,0.977,-0]
        self.ref_pose_4 = [-0.0373,0.11380,0.21,1.044,-2.963,0]
        self.ref_pose_5 = [-0.0296,0.0904,0.21,0.699,-3.06281,0]'''

        self.get_batch_ref_x_dist()
        self.iterator=0
        self.items=[]

    def get_batch_ref_x_dist(self):
        self.x_dist_batch_1 = self.ref_pose_2[0] - self.ref_pose_1[0]
        self.x_dist_batch_2 = self.ref_pose_4[0] - self.ref_pose_3[0]
        self.x_dist_batch_3 = self.ref_pose_6[0] - self.ref_pose_5[0]

    def get_batch_ref_pose_and_x_dist(self, batch_num):
        if batch_num == 1:
            return self.ref_pose_1, self.x_dist_batch_1
        elif batch_num == 2:
            return self.ref_pose_3, self.x_dist_batch_2
        elif batch_num == 3:
            return self.ref_pose_5, self.x_dist_batch_3
        return None, None

    def get_target_pose_rack(self, batch_num, rack_location):        
        batch_ref_pose, batch_x_dist = self.get_batch_ref_pose_and_x_dist(batch_num)
        if batch_ref_pose is not None:
            x_target_rack = batch_ref_pose[0] + (batch_x_dist * (rack_location-1))
            pose_to_sent = [x_target_rack, batch_ref_pose[1], batch_ref_pose[2], batch_ref_pose[3], batch_ref_pose[4], batch_ref_pose[5]]
            return  urlib.listToPose(pose_to_sent)
        return None


class GridCoagulation:
    # Parameterized Constructor
    def __init__(self, id, ref_pose_1, ref_pose_2, ref_pose_3, ref_pose_4, ref_pose_5,ref_pose_6, ref_pose_7, ref_pose_8):
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

    def get_angle(self, tube_location):
        return (tube_location-1) * self.angle


def testGridCoagulation():
    g = GridCoagulation(1,{'x':0.2621,'y':0.152,'z':-0.055,'rx':120,'ry':150,'rz':150}, {'x':0.521,'y':0.162,'z':-0.055,'rx':120,'ry':150,'rz':150}, 10)
    
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
    g = Grid(1,{'x': 0.020073328885008845, 'y': 0.02421647698344742, 'z': -0.01604996249824292, 'rx': -0.0001152386974497843, 'ry': -4.114015406898251e-05, 'rz': -7.946029271644992e-05}, 
    {'x': 0.04969106785988043, 'y': 0.02421647698344742, 'z': -0.01604996249824292, 'rx': -0.0001152386974497843, 'ry': -4.114015406898251e-05, 'rz': -7.946029271644992e-05},
    {'x': 0.020073328885008845, 'y': 0.05404200799125691, 'z': -0.01604996249824292, 'rx': -0.0001152386974497843, 'ry': -4.114015406898251e-05, 'rz': -7.946029271644992e-05}, 5, 8)
    #g = Grid(1,{'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
    #        {'x':110,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
    #        {'x':100,'y':120,'z':120,'rx':120,'ry':150,'rz':150},3,3)
    for i in range(40):
        print(i+1)
        r = g.get_target_x_y(i+1)
        print(r)
        print("----------------")
    
#testGrid()


def testGridBatch():
    g = GridBatch(1,{'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
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
    g = GridBatch(1,{'x':100,'y':100,'z':120,'rx':120,'ry':150,'rz':150},
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