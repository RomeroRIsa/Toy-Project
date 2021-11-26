from flask import Flask, render_template, Response, send_file, redirect, request
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
from io import BytesIO
import base64
import time

app = Flask(__name__)

# Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
   return render_template('test.html')

# Show Histograms
@app.route('/data', methods=['POST', 'GET'])
def generate_plot():
    img = BytesIO()
    select = request.form.get("distributions") # Option from user
    myTime = 0 
    start = time.time() #Start Time
    #Uniform Distribution
    if select == 'uniform':
      #start = time.time()
      
      # Generate random start and end points
      low = np.random.randint(1000)
      high = np.random.randint(low, 10000)
      
      #Generate data points
      uniformData = np.random.uniform(low,high, 10000)
      #end = time.time()
      
      #Plot
      plt.hist(uniformData, rwidth=0.95) 
      
      plt.savefig(img, format='png')
      plt.close()
      img.seek(0)

      plot_url = base64.b64encode(img.getvalue()).decode('utf8') 
    
    # Normal Distribution
    elif select == 'normal':
      #start = time.time()
      # Generate data points with random mean and std
      normalData = np.random.normal(np.random.randint(100), np.random.randint(100), 10000)
      #end = time.time()
      
      # Plot
      plt.hist(normalData, rwidth=0.95)
      plt.savefig(img, format='png')
      plt.close()
      img.seek(0)

      plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    # Normal distribution with mean and std from user
    elif select == 'normal_student':
      # Get mean and std from user
      desired_mean = request.form.get("mean")
      desired_std = request.form.get("std")
      
      # Convert to float
      desired_mean = float(desired_mean)
      desired_std = float(desired_std)

      #start = time.time()
      # Normal distribution with 0 mean and user std
      studentData = np.random.normal(loc=0.0, scale=desired_std, size=10000)
      actual_mean = np.mean(studentData)
      
      # Samples with zero mean
      zero_mean_samples = studentData - (actual_mean)

      zero_mean_std = np.std(zero_mean_samples)
      
      # Scale the samples with user std
      scaled_samples = zero_mean_samples * (desired_std/zero_mean_std)
      
      # add the user mean 
      final_samples = scaled_samples+desired_mean
      
      #end = time.time()
      
      # Plot
      plt.hist(final_samples, rwidth=0.95)
      plt.savefig(img, format='png')
      plt.close()
      img.seek(0)

      plot_url = base64.b64encode(img.getvalue()).decode('utf8')
      
    end = time.time() # End time
    myTime = end-start # get time needed to run
    myTime *= 1000 # get time in ms
    myTime = round(myTime,2) 

    return render_template('data.html', plot_url=plot_url, myTime=myTime)
    

if __name__ == '__main__':
   app.run()
