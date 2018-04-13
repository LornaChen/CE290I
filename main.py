#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 11:47:30 2018

@author: Lorna
"""
import skfmm
import numpy as np
import pylab as plt
import os

from flask import Flask
from flask import request, render_template
import requests
app = Flask(__name__)

@app.route("/")
def api290I():
    date = request.args.get('date')
    data_n = int(request.args.get('n'))
    r = requests.get('https://ce290-hw5-weather-report.appspot.com/', params={'date': date})
    dict = r.json()
    x=dict['centroid_x']
    y=dict['centroid_y']
    r=dict['radius']
    result=shortpath(x,y,r,data_n)
    img_path = 'static/path.png'
    return render_template('index.html', img_path = img_path, shortest_dist = result)


def shortpath(x,y,r,n):

    n=200
    phi=np.ones((n+1,n+1))
    phi[0,0]=0
    X, Y = np.meshgrid(np.linspace(0,20,n+1), np.linspace(0,20,n+1))
    mask = (X-10)**2+(Y-10)**2<=25
    phi  = np.ma.MaskedArray(phi, mask)
    d1=skfmm.distance(phi,dx=20/n)
    phi[0,0]=1
    phi[n,n]=0
    d2=skfmm.distance(phi,dx=20/n)
    d=d1+d2

    i=0
    j=0
    step=20/n
    x_path=[0]
    y_path=[0]
    x=0
    y=0
    plt.title('Shortest path from A to B')

    while i!=n and j!=n:
        m=min(d[i][j+1],d[i+1][j],d[i+1][j+1])
        if m==d[i+1][j]:
            i+=1
            x+=step
        elif m==d[i+1][j+1]:
            i+=1
            j+=1
            x+=step
            y+=step
        else:
            j+=1
            y+=step
        x_path.append(x)
        y_path.append(y)
    x_path.append(20)
    y_path.append(20)
    plt.contour(X, Y, phi,[0], linewidths=(3), colors='black')
    plt.contour(X, Y, d1, 40)
    plt.colorbar()
    plt.plot(y_path,x_path,'r')
    img_path = 'static/path.png'
    if os.path.isfile(img_path):
        os.remove(img_path)
    plt.savefig(img_path)
    plt.close('all')
    return (d1[n][n])

if __name__ == '__main__':
    app.run()
"""
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
"""
