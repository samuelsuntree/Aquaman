class CSV2DigitalTwin extends NACA {
    ArrayList < PVector[] > positionsList; // List to store positions for each time step
    ArrayList < PVector[] > spinePositionsList; // List to store spine positions for each time step
    ArrayList < float[] > spaceDerivativesList; // List to store the spatial derivatives
    //ArrayList < float[] > timeDerivativesList; // List to store the time derivates
    ArrayList < PVector > tcoords = new ArrayList < PVector > ();
    float[] averageAngles; // Array to store average angles for each time step
    int numColumns; // Number of columns in the tables
    int numRows; // Number of rows in the tables
    Table xTable, yTable, yFilteredTable; // CSV tables for x and y coordinates
    float startTime = 0; // Start time
    float endTime; // End time
    float currentTime = 0; // Current time for interpolation
    NACA orig; // Base on which to build the Digital Twin
    int index;
    float x0_dep = 0;
    float y0_dep = 0;

    // For test purpose only
    float[] a = {
        0,
        .2,
        -.1
    };
    float k, omega, T, xc, time = 0;
    float x_init = (int) pow(2, 6) / 4;
    float c = (int) pow(2, 6) / 3;
    int n_time = 0*100;

    CSV2DigitalTwin(float x0, float y0, int m, String xFilePath, String yFilePath, String yFilteredFilePath, Window window) {
        // Just as in flex NACA, set a regular NACA coords and save as orig
        super(x0 + 0.25 * (int) pow(2, 6) / 3, y0, (int) pow(2, 6) / 3, 0.2, m / 2, window);
        orig = new NACA(x0 + 0.25 * (int) pow(2, 6) / 3, y0, (int) pow(2, 6) / 3, 0.2, m / 2, window);

        // For test purpose only ----------------------------------------------------------------------------------
        // xc = x_init - 0.25*c;
        // k = TWO_PI/c;
        // omega = 1.2*k;
        // T = TWO_PI/omega;
        // float s = 0;
        // for(float ai: a) s+=ai;
        // if(s==0) {s=1; a[0]=1;}
        // for(int i=0; i<a.length; i++) a[i] *= 0.25*T/s;
        // --------------------------------------------------------------------------------------------------------

        // Load the coordinates
        xTable = loadTable(xFilePath);
        yTable = loadTable(yFilePath);
        yFilteredTable = loadTable(yFilteredFilePath);

        // Get the number of columns in the tables
        numColumns = xTable.getColumnCount();
        endTime = numColumns;

        // Get the number of rows in the tables
        if (xTable.getRowCount() != yTable.getRowCount()) {
            println("x and y tables are not the same size");
        }
        numRows = m;
        println("Rows: ", m, "; Columns: ", endTime);

        // Initialize the positionsList based on the number of columns
        positionsList = new ArrayList < PVector[] > (numColumns);
        spinePositionsList = new ArrayList < PVector[] > (numColumns); // Adjust the size of the list
        averageAngles = new float[numColumns];

        // Extract x and y coordinates from the tables and create points
        for (int i = n_time; i < numColumns; i++) { // Start from the n-th time step
            PVector[] positions = new PVector[numRows]; // Create an array for positions
            PVector[] spinePositions = new PVector[numRows / 2]; // Create an array for spine positions

            for (int j = 0; j < numRows; j++) {
                float x = xTable.getFloat(j, i); // Get x-coordinate from xTable
                float y = yTable.getFloat(j, i); // Get y-coordinate from yTable
                positions[j] = new PVector(x, y); // Create PVector and store it in positions array
            }
            // 计算 spine 位置
            for (int j = 0; j < numRows / 2; j++) {
                PVector p1 = positions[j];
                PVector p2 = positions[numRows - j - 1];
                spinePositions[j] = new PVector((p1.x + p2.x) / 2, (p1.y + p2.y) / 2);
            }
            positionsList.add(positions); // Add the positions array to the list
            spinePositionsList.add(spinePositions); // Add the spine positions array to the list
        }
        // 计算每个时间步的平均倾斜角度
        int numPointsToConsider = 5; // 假设我们考虑前5个点
        for (int t = 0; t < spinePositionsList.size(); t++) {
            PVector[] spinePositions = spinePositionsList.get(t);
            float totalAngle = 0;
            int count = 0;

            for (int i = 0; i < numPointsToConsider - 1; i++) {
                PVector p1 = spinePositions[i];
                PVector p2 = spinePositions[i + 1];

                float dx = p2.x - p1.x;
                float dy = p2.y - p1.y;

                float angle = atan2(dy, dx);
                totalAngle += angle;
                count++;
            }

            averageAngles[t] = totalAngle / count; // 存储平均角度
        }

        // Pre compute the spatial derivatives for every time step
        spaceDerivativesList = new ArrayList < float[] > (numColumns - n_time); // Adjust the size of the list
        for (int i = n_time; i < numColumns; i++) {
            float[] spaceDerivatives = new float[numRows];
            for (int j = 0; j < numRows; j++) {
                if (j == 0) { // Left border computation
                    spaceDerivatives[j] = spaceDerivative(j + 1, numRows - 1, i -  n_time);
                } else if (j == numRows - 1) { // Right border computation
                    spaceDerivatives[j] = spaceDerivative(0, j - 1, i -  n_time);
                } else {
                    spaceDerivatives[j] = spaceDerivative(j + 1, j - 1, i -  n_time);
                }
            }
            spaceDerivativesList.add(spaceDerivatives); // Add the derivatives array to the list
        }


        // Draw the first state by replacing the coordinates
        for (int k = 0; k < numRows; k++) {
            coords.get(k).x = positionsList.get(0)[k].x;
            coords.get(k).y = positionsList.get(0)[k].y;
        }
        end(true, true);
        PVector mn = positionsList.get(0)[0].copy(), mx = positionsList.get(0)[0].copy();
        for (int k = 0; k < positionsList.size(); k++) { // Ensure to use the correct range
            for (int i = 0; i < numRows; i++) {
                mn.x = min(mn.x, positionsList.get(k)[i].x);
                mn.y = min(mn.y, positionsList.get(k)[i].y);
                mx.x = max(mx.x, positionsList.get(k)[i].x);
                mx.y = max(mx.y, positionsList.get(k)[i].y);
            }
        }


        for (int i = 0; i < coords.size(); i++) {
            tcoords.add(new PVector(0, 0));
        }
    }





    PVector WallNormal(float x, float y) { // adjust orig normal
        PVector n = orig.WallNormal(x, y);
        n.x -= dhdx(x, y) * n.y;
        float m = n.mag();
        if (m > 0) return PVector.div(n, m);
        else return n;
    }

    float velocity(int d, float dt, float x, float y) { // use wave velocity
        float v = super.velocity(d, dt, x, y);
        if (x < (coords.get(0).x - 70) || x > coords.get(coords.size() - 1).x + 70 || y < (coords.get(0).y - 70) || y > (coords.get(0).y + 70)) {
            return v;
        } else {
            int i = on_which_boundary_new(x, y);
            float v_x = v;
            float v_y = v;
            if (i < 0 || i > (coords.size() - 1)) {
                if (d == 1) {
                    //println("Vx = ", (v+hdot(x)), " X = ", x, " Y = ",y);
                    return v_x;
                } else return v_y;
            } else if (i == (coords.size() - 1)) {
                v_x = (coords.get(i).x + coords.get(0).x - tcoords.get(i).x - tcoords.get(0).x) / (2 * dt);
                v_y = (coords.get(i).y + coords.get(0).y - tcoords.get(i).y - tcoords.get(0).y) / (2 * dt);
                if (d == 1) {
                    //println("Vx = ", (v+hdot(x)), " X = ", x, " Y = ",y);
                    return v_x;
                } else return v_y;
            } else {
                v_x = (coords.get(i).x + coords.get(i + 1).x - tcoords.get(i).x - tcoords.get(i + 1).x) / (2 * dt);
                v_y = (coords.get(i).y + coords.get(i + 1).y - tcoords.get(i).y - tcoords.get(i + 1).y) / (2 * dt);
                if (d == 1) {
                    //println("Vx = ", (v+hdot(x)), " X = ", x, " Y = ",y);
                    return v_x;
                } else return v_y;
            }
        }
    }
    int on_which_boundary_new(float x, float y) {
        if (x < (coords.get(0).x - 70) || x > coords.get(coords.size() - 1).x + 70 || y < (coords.get(0).y - 70) || y > (coords.get(0).y + 70)) {
            return int(-1); //far from edge
        } else {
            int index = 0;
            int min_index = 0;
            float dis = 1e10, dis_temp;
            for (PVector o: coords) {
                dis_temp = pow((x - o.x), 2) + pow((y - o.y), 2);
                if (dis_temp < dis) {
                    dis = dis_temp;
                    min_index = index;
                }
                index++;
            };
            if (dis < 1.0)
                return min_index;
            else
                return -1;
        }
    }

    void translate(float dx, float dy) {
        super.translate(dx, dy);
        orig.translate(dx, dy);
        x0_dep += dx;
        y0_dep += dy;
    }

    void rotate(float dphi) {} // no rotation

    void update(float time) { // update 'time' and coords

        // Calculate the index based on currentTime
        int index = (int)(time / 0.686778 - 1);
        this.index = index;
        this.time = time;

        if (index < numColumns - 100) {
            for (int i = 0; i < numRows; i++) coords.set(i, orig.coords.get(i).copy());
            if (index - 1 < 0) {
                box.translate(0, 0);
                //box.rotate(averageAngles[index], spinePositionsList.get(index)[20]);
            } else {
                //orig.end();
                box.translate(-positionsList.get(index - 1)[0].x + positionsList.get(index)[0].x, 0*(-positionsList.get(index - 1)[0].y + positionsList.get(index)[0].y));
                //box.rotate(averageAngles[index]-averageAngles[index-1], spinePositionsList.get(index)[20]);
            }
            for (int k = 0; k < numRows; k++) {
                coords.get(k).x = x0_dep + positionsList.get(index)[k].x;
                coords.get(k).y = y0_dep + positionsList.get(index)[k].y;
                if (index - 1 < 0) {
                    tcoords.get(k).x = x0_dep + positionsList.get(0)[k].x;
                    tcoords.get(k).y = y0_dep + positionsList.get(0)[k].y;
                    println(k + "  " + (index - 1));
                } else {
                    tcoords.get(k).x = x0_dep + positionsList.get(index - 1)[k].x;
                    tcoords.get(k).y = y0_dep + positionsList.get(index - 1)[k].y;
                }

            }
            //end();
            // Update currentTime
            currentTime += 1;
            if (currentTime > endTime) {
                currentTime = startTime;
            }
        }
        getOrth();
    }

    boolean unsteady() {
        return true;
    }

    // With this geometry, we don't know the global deformation
    // We thus have to approximate the derivative numerically: dy/dx = y(n+1)-y(n-1)/2DeltaX

    float spaceDerivative(int a, int b, int c) {
        if (xTable.getFloat(a, c) == xTable.getFloat(b, c)) {
            return 1e10;
        } else {
            return (yTable.getFloat(a, c) - yTable.getFloat(b, c)) / (xTable.getFloat(a, c) - xTable.getFloat(b, c));
        }
    }

    float dhdx(float x, float y) {
        // Find the closest point to (x,y) to get the corresponding local derivative
        PVector[] currentPosSpaceD = positionsList.get(index);
        int pt_index = 0;
        float min_dis = 1e10;
        for (int i = 0; i < currentPosSpaceD.length; i++) {
            if (dist(x, y, currentPosSpaceD[i].x, currentPosSpaceD[i].y) < min_dis) {
                pt_index = i;
                min_dis = dist(x, y, currentPosSpaceD[i].x, currentPosSpaceD[i].y);
            }
        }
        float coef_derivative = spaceDerivativesList.get(index)[pt_index];
        return coef_derivative;
    }


}