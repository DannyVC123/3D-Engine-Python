# 3D-Engine-Python
A 3D Engine created in Python with minimal use of built-in graphics libraries. I coded all the linear algebra operations.

Initially inspred by mattbatwings "I Made a 3D Renderer with just redstone!"

[![Watch the video](https://img.youtube.com/vi/hFRlnNci3Rs/maxresdefault.jpg)](https://youtu.be/hFRlnNci3Rs)

# Progress
## 3D Projection
- Converts 3D objects onto a 2D screen
- **Math:** [Weak Perspective Projection](https://en.wikipedia.org/wiki/3D_projection#Weak_perspective_projection)
- **Tutorial:** [I Made a 3D Renderer with just redstone! (mattbatwings)](https://youtu.be/hFRlnNci3Rs)

## 3D Rotation
- Rotates vertices by any angle *θ* around any unit vector **u** by clicking and dragging the 3D model
- **Math:** [3D rotation matrix from axis and angle](https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle)
- **Tutorial:** [I Made a 3D Renderer with just redstone! (mattbatwings)](https://youtu.be/hFRlnNci3Rs), Wikipedia (see above)

## Filled Polygons v0
- Colors in each polygon of the model using the built in pygame.draw.polygon function
- **Math:** None
- **Tutorial:** None

## Backface Culling
- Does not render faces oriented away from the camera
- **Math:** [Surface Normal Dot Product](https://en.wikipedia.org/wiki/Back-face_culling#Implementation)
- **Tutorial:** [3D Programming Fundamentals [Backface Culling] (ChiliTomatoNoodle)](https://youtu.be/h_Aqol0oTs4)

## Flat Shading
- Dynamic lighting for each face of the model
- **Math & Tutorial:** [3D Programming Fundamentals [Flat Shading] (ChiliTomatoNoodle)](https://youtu.be/wOyavGx28uU)
