File tan.c contains tests for tan() function from standard C library (phoenix).

Using the equivalence classes the set [-pi/2; pi/2] was tested as input data.
There was used boundary values analysis, chosen input:
- limit values that are outside the proper input set (-pi/2 and pi/2)
- values that are inside the domain and are close enough to the limits that can be called 'boundary values' (-pi/2+10e-6 and pi/2-10e-6)

To make the test complete the middle values from the input set were also tested.
Tasts were executed with set precision of 10e-9.
