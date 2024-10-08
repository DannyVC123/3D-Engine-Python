# Python 3D Engine
A 3D Engine created in Python with minimal use of built-in graphics libraries. All linear algebra operations were implemented manually.

Initially inspred by mattbatwings "[I Made a 3D Renderer with just redstone!](https://youtu.be/hFRlnNci3Rs)"

[![Watch the video](https://img.youtube.com/vi/hFRlnNci3Rs/maxresdefault.jpg)](https://youtu.be/hFRlnNci3Rs)

# 3D Engine Progress
## 3D Projection
- Converts 3D objects onto a 2D screen
- Uses `pygame.draw.polygon` to color faces
- **Math:** [Weak Perspective Projection](https://en.wikipedia.org/wiki/3D_projection#Weak_perspective_projection)
- **Tutorial:** [I Made a 3D Renderer with just redstone! (mattbatwings)](https://youtu.be/hFRlnNci3Rs)

<img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/00_wireframe.jpg" style="height:300px;"/><img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/01_colored.jpg" style="height:300px;"/>

## 3D Rotation
- Rotates vertices by any angle *θ* around any unit vector **u** by clicking and dragging the 3D model
- **Math:** [3D rotation matrix from axis and angle](https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle)
- **Tutorial:** [I Made a 3D Renderer with just redstone! (mattbatwings)](https://youtu.be/hFRlnNci3Rs), Wikipedia (see above)

<img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/10_rot_0.jpg" style="height:200px;"/><img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/11_rot_1.jpg" style="height:200px;"/><img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/12_rot_2.jpg" style="height:200px;"/>

## Backface Culling
- Does not render faces oriented away from the camera
- Does not work for convex shapes (see bowl model below)
- **Math:** [Surface Normal Dot Product](https://en.wikipedia.org/wiki/Back-face_culling#Implementation)
- **Tutorial:** [3D Programming Fundamentals [Backface Culling] (ChiliTomatoNoodle)](https://youtu.be/h_Aqol0oTs4)

<img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/20_cube.jpg" style="height:200px;"/><img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/21_soccer_ball.jpg" style="height:200px;"/><img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/22_bowl.jpg" style="height:200px;"/>

## Flat Shading
- Dynamic lighting for each face of the model
- **Math:** [Lambertian Reflectance](https://en.wikipedia.org/wiki/Lambertian_reflectance#Use_in_computer_graphics)
- **Tutorial:** [3D Programming Fundamentals [Flat Shading] (ChiliTomatoNoodle)](https://youtu.be/wOyavGx28uU)

## Triangle Rasterization
- Fills each triangle by calculating which pixels lie within the three edges using the [top-left rule](https://en.wikipedia.org/wiki/Rasterisation#Triangle_rasterization)
- Uses `pygame.PixelArray` instead of `pygame.draw.polygon`
- Triangles have to be calculated manually
- Doesn't look as clean as `pygame.draw.polygon` but is implemented without libraries and allows for features such as texture mapping
- **Math:** [Linear equations](https://www.mathsisfun.com/algebra/line-equation-2points.html)
- **Tutorial:** [3D Programming Fundamentals [Triangle Rasterization] (ChiliTomatoNoodle)](https://youtu.be/9A5TVh6kPLA)

<img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/4_triangles.jpg" style="height:300px;"/>

## Polygon Triangulation
- Converts each 2D face into a set of triangles for rasterization
- Examples shown below (left: `pygame.draw.polygon`, right: triangulation and rasterization)
- **Algorithm:** [Ear Clipping](https://en.wikipedia.org/wiki/Polygon_triangulation#Ear_clipping_method)
- **Tutorial:** [Polygon Triangulation - Overview of Ear Clipping (Two-Bit Coding)](https://www.youtube.com/watch?v=QAdfkylpYwc&ab_channel=Two-BitCoding)

<img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/50_soccer_ball.jpg" style="height:200px;"/>

<img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/51_umbrella_no_riangles.jpg" style="height:200px;"/><img src="https://github.com/DannyVC123/3D-Engine-Python/blob/main/res/images/screenshots/52_umbrella_w_triangles.jpg" style="height:200px;"/>


<br/><br/>

# .obj Files
## Read .obj files
- Render any 3D model of the .obj file format

## (Near-optimal) Bounding Sphere
- Calculates a near-optimal sphere that encloses all the vertices in a 3D model
- Used to translate the model to be centered at the origin
- Algorithm: [Ritter's bounding sphere](https://www.researchgate.net/publication/242453691_An_Efficient_Bounding_Sphere)
