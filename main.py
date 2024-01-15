from typing import List
from fastapi import FastAPI, HTTPException

app = FastAPI()


def is_valid_matrix(matrix):
    return all(len(row) == len(matrix[0]) for row in matrix)


def largest_rectangle(matrix: List[List[int]]) -> tuple:
    if not matrix or not matrix[0]:
        raise HTTPException(status_code=400, detail="Input matrix is empty")

    if not is_valid_matrix(matrix):
        raise HTTPException(status_code=400, detail="Invalid matrix: Rows have different lengths")

    rows, cols = len(matrix), len(matrix[0])
    max_area = 0
    max_num = None

    for i in range(rows):
        for j in range(cols):
            current_num = matrix[i][j]
            current_area = 0

            for k in range(i, rows):
                for l in range(j, cols):
                    if matrix[k][l] == current_num:
                        current_area += 1
                    else:
                        break

            if current_area > max_area:
                max_area = current_area
                max_num = current_num

    return max_num, max_area


@app.post("/largest_rectangle")
async def get_largest_rectangle(data: dict):
    try:
        matrix = data.get("matrix")
        result = largest_rectangle(matrix)
        return {"max_num": result[0], "max_area": result[1]}
    except HTTPException as e:
        return {"error": e.detail}

# Test Case 1 - Valid Matrix
# Invoke-WebRequest -Uri "http://127.0.0.1:8000/largest_rectangle" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"matrix": [[1, 1, 1, 0, 1, -9], [1, 1, 1, 1, 2, -9], [1, 1, 1, 1, 2, -9], [1, 0, 0, 0, 5, -9], [5, 0, 0, 0, 5, 9]]}' -UseBasicParsing
# <---------------{"max_num":1,"max_area":12}




# Test Case 2 - Empty Matrix (Expecting Error)
# Invoke-WebRequest -Uri "http://127.0.0.1:8000/largest_rectangle" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"matrix": []}' -UseBasicParsing
# <---------------{"error":"Input matrix is empty"}



# Test Case 3 - Matrix with Single Element
# Invoke-WebRequest -Uri "http://127.0.0.1:8000/largest_rectangle" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"matrix": [[1]]}' -UseBasicParsing
# <---------------{"max_num":1,"max_area":1}


# Test Case 4 - Matrix with All Zeros
# Invoke-WebRequest -Uri "http://127.0.0.1:8000/largest_rectangle" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"matrix": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]}' -UseBasicParsing
#  --------------->{"max_num":0,"max_area":9}


# Test Case 5 - Matrix with Negative Numbers
# Invoke-WebRequest -Uri "http://127.0.0.1:8000/largest_rectangle" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"matrix": [[-1, -1, -1], [-1, -2, -1], [-1, -1, -1]]}' -UseBasicParsing
# --------------->{"max_num":-1,"max_area":7}


