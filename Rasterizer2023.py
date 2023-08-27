from gl import Renderer, Model
import shaders


# El tama�o del FrameBuffer
width = 960
height = 540

# Se crea el renderizador
rend = Renderer(width, height)

""" rend.glClearColor(0.2,0.2,0.2)
rend.glClear() """

rend.glBackgroundTexture("textures/fondo.bmp")
rend.glClearBackground()

rend.directionalLight=(0.5,-0.3,-0.8)

rend.glLookAt(camPos=(0, 2, 0),
              eyePos=(0,2,-5))

model1= Model("models/desk.obj",
             translate = (-5.7, -1.2, -10),
             rotate = (0, 0, 0),
             scale = (0.5,0.7,0.5))
model1.LoadTexture("textures/wood.bmp")
model1.SetShaders(shaders.vertexShader, shaders.gouradShader)

model2= Model("models/Box.obj",
             translate = (-1.5, 1.2, -10),
             rotate = (0, -8, 180),
             scale = (0.07,0.08,0.07))
model2.LoadTexture("textures/caja.bmp")
model2.SetShaders(shaders.vertexShader, shaders.woodShader)

model3= Model("models/impresora.obj",
               translate= (-1.4, 1.3, -10),
               rotate= (-90,0,0),
               scale=(0.05,0.05,0.05))
model3.LoadTexture("textures/impresora.bmp")
model3.SetShaders(shaders.vertexShader, shaders.plasticShader)

model4= Model("models/monitor.obj",
               translate= (-5.9,3.2,-8),
               rotate= (0,10,0),
               scale=(1.3,1.3,1.3))
model4.LoadTexture("textures/monitor.bmp")
model4.SetShaders(shaders.vertexShader, shaders.gouradShader)

model5= Model("models/Box.obj",
             translate = (5.1, 0.7, -9.3),
             rotate = (0, -8, 180),
             scale = (0.2,0.06,0.07))
model5.LoadTexture("textures/caja.bmp")
model5.SetShaders(shaders.vertexShader, shaders.woodShader)

model6= Model("models/coco.obj",
             translate = (6, 0.7, -9),
             rotate = (-90, 0, 75),
             scale = (0.03,0.03,0.03))
model6.LoadTexture("textures/cocodrilo.bmp")
model6.SetShaders(shaders.vertexShader, shaders.snakeShader)

model7= Model("models/cuadro.obj",
             translate = (6, 4.5, -9),
             rotate = (0,-90,0),
             scale = (4,4,4))
model7.LoadTexture("textures/cuadro.bmp")
model7.SetShaders(shaders.vertexShader, shaders.oilPaintingShader)

model8= Model("models/cuadro.obj",
             translate = (2.5, 4.5, -9),
             rotate = (0,-90,0),
             scale = (4,4,4))
model8.LoadTexture("textures/cuadro.bmp")
model8.SetShaders(shaders.vertexShader, shaders.gouradShader)

rend.glAddModel(model1)
rend.glAddModel(model2)
rend.glAddModel(model3) 
rend.glAddModel(model4)
rend.glAddModel(model5)
rend.glAddModel(model6)
rend.glAddModel(model7)
rend.glAddModel(model8)

# Se renderiza la escena
rend.glRender()

# Se crea el FrameBuffer con la escena renderizada
rend.glFinish("shaders/livingroom.bmp")