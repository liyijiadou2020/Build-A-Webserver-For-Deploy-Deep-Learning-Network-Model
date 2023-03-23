from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # 文件夹的名字必须叫templates，放在同一个目录下
    # 还可以向http传递参数
    # return render_template('index.html', title="Flask Web App")

    # 利用循环和判断控制template的渲染,在html文件中写
    # return render_template('index.html')
    # 传入列表
    # data=['cat', 'dog', 'monkey', 'hellokitty']
    # return render_template('index.html', data=data)

    # 模板的继承
    return render_template('index.html')



if __name__=='__main__':
    # app.run() # 如果修改了文件，需要重新启动server
    # app.run(debug=True) # 修改文件不需要重启server也可以反映出代码的变化
    app.run(debug=True, host="0.0.0.0", port=3000)
