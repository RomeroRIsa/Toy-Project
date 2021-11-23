from flask import Flask, render_template, Response, send_file, redirect, request
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
from io import BytesIO
import base64
import time

app = Flask(__name__)

@app.route('/hello')
def hello_world():
   return "Hello World"

@app.route('/', methods=['POST', 'GET'])
def index():
   return render_template('test.html')

@app.route('/data', methods=['POST', 'GET'])
def generate_plot():
    img = BytesIO()
    select = request.form.get("distributions")
    myTime = 0
    start = time.time()
    if select == 'uniform':
      #start = time.time()
      low = np.random.randint(1000)
      high = np.random.randint(low, 10000)

      uniformData = np.random.uniform(low,high, 10000)
      #end = time.time()
      
      plt.hist(uniformData, rwidth=0.95) 
      
      plt.savefig(img, format='png')
      plt.close()
      img.seek(0)

      plot_url = base64.b64encode(img.getvalue()).decode('utf8')
      
    elif select == 'normal':
      #start = time.time()
      normalData = np.random.normal(np.random.randint(100), np.random.randint(100), 10000)
      #end = time.time()
      plt.hist(normalData, rwidth=0.95)
      plt.savefig(img, format='png')
      plt.close()
      img.seek(0)

      plot_url = base64.b64encode(img.getvalue()).decode('utf8')
      
    elif select == 'normal_student':
      desired_mean = request.form.get("mean")
      desired_std = request.form.get("std")
      desired_mean = float(desired_mean)
      desired_std = float(desired_std)

      #start = time.time()
      studentData = np.random.normal(loc=0.0, scale=desired_std, size=10000)
      actual_mean = np.mean(studentData)

      zero_mean_samples = studentData - (actual_mean)

      zero_mean_std = np.std(zero_mean_samples)

      scaled_samples = zero_mean_samples * (desired_std/zero_mean_std)
    
      final_samples = scaled_samples+desired_mean
      #end = time.time()
      plt.hist(final_samples, rwidth=0.95)
      plt.savefig(img, format='png')
      plt.close()
      img.seek(0)

      plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    end = time.time()
    myTime = end-start 
    myTime *= 1000
    myTime = round(myTime,2)    

    return render_template('data.html', plot_url=plot_url, myTime=myTime)
    

if __name__ == '__main__':
   app.run()