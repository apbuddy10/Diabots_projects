import math
# import matplotlib.pyplot as plt

class Grid():
    def __init__(self,pose_1,pose_2,pose_3,row,col):
        self.pose_1 = pose_1
        self.pose_2 = pose_2
        self.pose_3 = pose_3
        self.row = row
        self.col = col
        self.m_slope_p1_p2 = self.get_slope_xy(self.pose_1,self.pose_2)
        self.m_slope_p1_p3 = self.get_slope_xy(self.pose_1,self.pose_3)
        self.xd_yd_dir_arr_p1_p2 = self.get_Xd_Yd(self.pose_1,self.pose_2,self.col)
        self.xd_yd_dir_arr_p1_p3 = self.get_Xd_Yd(self.pose_1,self.pose_3,self.row)
        self.final_arr = self.get_final_arr()

    def get_slope_xy(self,pose_1,pose_2):
        X1 = pose_1[0]
        Y1 = pose_1[1]
        X2 = pose_2[0]
        Y2 = pose_2[1]

        if( X1 != X2 ):
            m_slope = (Y2 - Y1)/(X2 - X1)
            return m_slope
        else:
            return math.inf  

    def get_Xd_Yd(self,point_1,point_2,num):
        X1 = point_1[0] # start X1
        Y1 = point_1[1] # start Y1
        X2 = point_2[0] # end X2
        Y2 = point_2[1] # end Y2
        X_dir = None
        Y_dir = None
        if( X1 < X2 ):
            Xd = (X2 - X1) / (num - 1 )
            X_dir = True # +ve
        elif(X1 > X2):
            Xd = (X1 - X2)/ (num - 1)
            X_dir = False # -ve
        else:
            Xd = 0
            X_dir = None # zero
        if( Y1 < Y2 ):
            Yd = (Y2 - Y1) / (num - 1) 
            Y_dir = True # +ve
        elif(Y1 > Y2):
            Yd = (Y1 - Y2)/ (num - 1)
            Y_dir = False # -ve
        else:
            Yd = 0
            Y_dir = None # zero

        return [Xd,Yd,X_dir,Y_dir,num]


    def get_x_y_coordinates(self,point_1,xd_yd_dir_arr,m_slope):
        X1 = point_1[0] # start X1
        Y1 = point_1[1] # start Y1
        # X2 = point_2[0] # end X2
        # Y2 = point_2[1] # end Y2
        Z1 = self.pose_1[2]
        Rx = self.pose_1[3]
        Ry = self.pose_1[4]
        Rz = self.pose_1[5]

        Xd = xd_yd_dir_arr[0]
        Yd = xd_yd_dir_arr[1]
        X_dir = xd_yd_dir_arr[2]
        Y_dir = xd_yd_dir_arr[3]
        num = xd_yd_dir_arr[4]

        C_intercept = None
        coordArr_x_y = []

        if(m_slope != math.inf):
            C_intercept = Y1 - (m_slope * X1)

            if( X_dir == True ):
                # Xd = (X2 - X1) / (num - 1)
                for loop_cnt in range(num):
                    X_res = X1 + (loop_cnt * Xd)
                    Y_res = m_slope * (X_res) + C_intercept
                    coordArr_x_y.append([X_res,Y_res,Z1,Rx,Ry,Rz])
                return coordArr_x_y
            elif(X_dir == False):
                # Xd = (X1 - X2)/ (num - 1)
                for loop_cnt in range(num):
                    X_res = X1 - (loop_cnt * Xd)
                    Y_res = m_slope * (X_res) + C_intercept
                    coordArr_x_y.append([X_res,Y_res,Z1,Rx,Ry,Rz])
                return coordArr_x_y
            elif(X_dir == None):
                Xd = 0
                for loop_cnt in range(num):
                    X_res = X1 + (loop_cnt * Xd)
                    Y_res = Y1
                    coordArr_x_y.append([X_res,Y_res,Z1,Rx,Ry,Rz])
                return coordArr_x_y
        else:
            if( Y_dir == True ):
                # Yd = (Y2 - Y1) / (num - 1)
                for loop_cnt in range(num):
                    X_res = X1 
                    Y_res = Y1 + loop_cnt * Yd
                    coordArr_x_y.append([X_res,Y_res,Z1,Rx,Ry,Rz])
                return coordArr_x_y
            elif(Y_dir == False):
                # Yd = (Y1 - Y2)/ (num - 1)
                for loop_cnt in range(num):
                    X_res = X1 
                    Y_res = Y1 - loop_cnt * Yd
                    coordArr_x_y.append([X_res,Y_res,Z1,Rx,Ry,Rz])
                return coordArr_x_y
            elif(Y_dir == None):
                Yd = 0
                for loop_cnt in range(num):
                    X_res = X1 
                    Y_res = Y1
                    coordArr_x_y.append([X_res,Y_res,Z1,Rx,Ry,Rz])
                return coordArr_x_y

    def get_final_arr(self):
        coordArr_p1_p3 = self.get_x_y_coordinates(self.pose_1,self.xd_yd_dir_arr_p1_p3,self.m_slope_p1_p3)
        coordArr_final = []
        for row_cnt in range(self.row):
            coordArr = self.get_x_y_coordinates(coordArr_p1_p3[row_cnt],self.xd_yd_dir_arr_p1_p2,self.m_slope_p1_p2)
            for col_cnt in range(self.col):
                coordArr_final.append(coordArr[col_cnt])
        return coordArr_final

    def get_target_x_y(self,indx):
        return self.final_arr[indx-1]
    

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

    def get_target_x_y(self , parent_grid_location, child_grid_location):
        par_loc = self.parent_grid.get_target_x_y(parent_grid_location)
        child_loc = self.child_grid.get_target_x_y(child_grid_location)
        x_ret_loc = par_loc[0]+(child_loc[0]-self.ref_pose_1[0])
        y_ret_loc = par_loc[1]+(child_loc[1]-self.ref_pose_1[1])
        return [x_ret_loc, y_ret_loc, par_loc[2], par_loc[3], par_loc[4], par_loc[5]]

def main():
    gridClassPlane = Grid([0,0,1,2,3,4,5],[6,0,1,2,3,4,5],[0,6,1,2,3,4,5],3,5) # test 1
    final_arr = gridClassPlane.get_final_arr()
    # gridClassPlane = GridClassPlane([0,0],[-6,0],[0,5],6,7) # test 2
    # final_arr = gridClassPlane.get_final_arr()
    # gridClassPlane = GridClassPlane([0,0],[-6,0],[0,-5],6,7) # test 3
    # final_arr = gridClassPlane.get_final_arr()
    # gridClassPlane = GridClassPlane([0,0],[6,0],[0,-5],6,7) # test 4
    # final_arr = gridClassPlane.get_final_arr()

    # gridClassPlane = GridClassPlane([-100,-13],[44,1],[-22,5],6,7) # test 2
    # final_arr = gridClassPlane.get_final_arr()
    
    location  = gridClassPlane.get_target_x_y(0)
    print(location)
    print(final_arr)
    # for arr in final_arr:
    #     plt.plot(arr[0], arr[1],'o')
    # plt.show()

if __name__ == '__main__':
    main()