#Import necessary libraries
from flask import Flask, render_template, request
import numpy as np
import os
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

# Specify the path of the model
filepath = '/Users/needapsychiatrist/Desktop/Web_App/model.h5'
# Loading Model
model = load_model(filepath)

# Prompt - Executes only if model is loaded successfully
print("Model Loaded Successfully!")

# Method
def predictionMethod(tomatoLeaf):
  test_image = load_img(tomatoLeaf, target_size = (128, 128)) # Loading image  
  test_image = img_to_array(test_image)/255 # Converting image to np array and normalize
  test_image = np.expand_dims(test_image, axis = 0) # Change dimention 3D to 4D
  
  result = model.predict(test_image) # Predicting diseased leaf
  
  pred = np.argmax(result, axis=1)

  if pred==0:
      return "ঢলে পড়া (Bacterial Spot)", 'Tomato - Bacteria_Spot.html'
       
  elif pred==1:
      return "আগাম ধসা (Early blight)", 'Tomato - Early_Blight.html'
        
  elif pred==2:
      return "স্বাস্থ্যবান এবং রোগবালাই বিহীন", 'Tomato - Healthy.html'
        
  elif pred==3:
      return "নাবি ধসা (Late blight)", 'Tomato - Late_Blight.html'
       
  elif pred==4:
      return "ফিউজারিয়াম ঢলে পড়া (Mold Disease)", 'Tomato - Leaf_Mold.html'
        
  elif pred==5:
      return "হলুদ মোজাইক (Septoria Spot)", 'Tomato - Septoria_Leaf_Spot.html'
        
  elif pred==6:
      return "বিশেষ আগাম ধসা (Target Spot)", 'Tomato - Target_Spot.html'
        
  elif pred==7:
      return "পাতা কুঁকড়ানো (Leaf curl)", 'Tomato - Tomato_Yellow_Leaf_Curl_Virus.html'

  elif pred==8:
      return "মোজাইক (Mosaic Virus)", 'Tomato - Tomato_Mosaic_Virus.html'
        
  elif pred==9:
      return "দুই দাগযুক্ত স্পাইডার মাইট (Two Spotted Spider Mite Disease)", 'Tomato - Two_Spotted_Spider_Mite.html'

    
# Create flask instance
app = Flask(__name__)

# Render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')

@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] 
        filename = file.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join('/Users/needapsychiatrist/Desktop/Web_App/static/upload/', filename)
        file.save(file_path)

        pred, output_page = predictionMethod(tomatoLeaf=file_path)
              
        return render_template(output_page, pred_output = pred, user_image = file_path)
    
# For local system & cloud
if __name__ == "__main__":
    app.run(threaded=False,port=8080) 
    
    
