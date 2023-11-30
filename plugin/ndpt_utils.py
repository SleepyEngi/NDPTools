def vectorisclose(vector1, vector2, tolerance=0.0001):
    # Determine if the inputs are correctly utilized.
    if not isinstance(vector1, Vector) or not isinstance(vector2, Vector) or not isinstance(tolerance, float):
        raise TypeError("Input 1 must be a vector. Input 2 must be a vector. Input 3 must be a float.")
    # Compare the components of the vectors.
    if len(vector1) != len(vector2):
        raise TypeError("Both vectors must have the same amount of components")
    # Compare components
    for component in range(0, len(vector1)):
        if not abs(vector1[component] - vector2[component]) < abs(tolerance):
            return False
    return True