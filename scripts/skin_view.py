import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

def head(img,k,ax,p):
    xp=8
    yp=8
    head1_front=img[p:2*p,p:2*p]
    head2_front=img[p:2*p,5*p:6*p]
    head1_top=img[:p,p:2*p]
    head2_top=img[:p,5*p:6*p]

    head1_bottom=img[:p,2*p:3*p]
    head2_bottom=img[:p,6*p:7*p]

    head1_right=img[p:2*p,:p]
    head2_right=img[p:2*p,4*p:5*p]
    head1_left=img[p:2*p,2*p:3*p]
    head2_left=img[p:2*p,6*p:7*p]

    head1_back=img[p:2*p,3*p:4*p]
    head2_back=img[p:2*p,7*p:8*p]

    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-4
    y=y-4
    Y, X = np.meshgrid(y, x)

    #head
    #x,y平面(上面)
    ax.plot_surface(X, Y, X-X+(yp/2)+24, facecolors=np.fliplr(head1_top.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X*k, Y*k, X-X+(yp*k/2)+24, facecolors=np.fliplr(head2_top.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #底面
    ax.plot_surface(X, Y, X-X-(yp/2)+24, facecolors=np.fliplr(head1_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X*k, Y*k, X-X-(yp*k/2)+24, facecolors=np.fliplr(head2_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    #x,z平面(正面)
    ax.plot_surface(Y, X-X-yp/2, X+24, facecolors=np.flipud(head1_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k, X-X-yp*k/2, X*k+24, facecolors=np.flipud(head2_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
        #背面
    ax.plot_surface(Y, X-X+yp/2, X+24, facecolors=np.fliplr(np.flipud(head1_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k, X-X+yp*k/2, X*k+24, facecolors=np.fliplr(np.flipud(head2_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    #y,z平面
    ax.plot_surface(X-X+int(xp/2), X, Y+24, facecolors=np.fliplr(head1_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X+(xp*k/2), X*k, Y*k+24, facecolors=np.fliplr(head2_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #右面
    ax.plot_surface(X-X-int(xp/2), X, Y+24, facecolors=np.flipud(np.fliplr(head1_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X-(xp*k/2), X*k, Y*k+24, facecolors=np.flipud(np.fliplr(head2_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
def body(img,k,ax,q):
    z=14
    body1_front=img[5*q:8*q,5*q:7*q]
    body2_front=img[9*q:12*q,5*q:7*q]
    body1_top=img[4*q:5*q,5*q:7*q]
    body2_top=img[8*q:9*q,5*q:7*q]

    body1_bottom=img[4*q:5*q,7*q:9*q]
    body2_bottom=img[8*q:9*q,7*q:9*q]

    body1_right=img[5*q:8*q,4*q:5*q]
    body2_right=img[9*q:12*q,4*q:5*q]

    body1_left=img[5*q:8*q,7*q:8*q]
    body2_left=img[9*q:12*q,7*q:8*q]

    body1_back=img[5*q:8*q,8*q:10*q]
    body2_back=img[9*q:12*q,8*q:10*q]
    #一回transposeしてるから逆になる
    xp=8
    yp=4
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    #print(x,y)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)
    #print(X,Y)
    #head
    #x,y平面(上面)
    #print(Y.shape)
    #print(np.fliplr(body1_top.transpose((1,0,2))).shape)
    ax.plot_surface(X, Y, X-X+6+z, facecolors=np.fliplr(body1_top.transpose((1,0,2))),
            rstride=1, cstride=1,
            antialiased=True, shade=False)
    ax.plot_surface(X*k, Y*k, X-X+6*k+z, facecolors=np.fliplr(body2_top.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #底面
    ax.plot_surface(X, Y, X-X-6+z, facecolors=np.fliplr(body1_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X*k, Y*k, X-X-6*k+z, facecolors=np.fliplr(body2_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    xp=12
    yp=8
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)    
    #x,z平面(正面)
    ax.plot_surface(Y, X-X-2, X+z, facecolors=np.flipud(body1_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k, X-X-2*k, X*k+z, facecolors=np.flipud(body2_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
        #背面
    ax.plot_surface(Y, X-X+2, X+z, facecolors=np.fliplr(np.flipud(body1_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k, X-X+k*2, X*k+z, facecolors=np.fliplr(np.flipud(body2_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
     #一回transposeしてるから逆になる
    xp=4
    yp=12
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)    
    #y,z平面
    ax.plot_surface(X-X+4, X, Y+z, facecolors=np.fliplr(body1_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X+4*k, X*k, Y*k+z, facecolors=np.fliplr(body2_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #右面
    ax.plot_surface(X-X-4, X, Y+z, facecolors=np.flipud(np.fliplr(body1_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X-4*k, X*k, Y*k+z, facecolors=np.flipud(np.fliplr(body2_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
def right_hand(img,k,ax,q,iswide):
    z=14
    d=6
    if iswide:
        rh1_front=img[5*q:8*q,11*q:12*q]
        rh2_front=img[9*q:12*q,11*q:12*q]
        rh1_top=img[4*q:5*q,11*q:12*q]
        rh2_top=img[8*q:9*q,11*q:12*q]

        rh1_bottom=img[4*q:5*q,12*q:13*q]
        rh2_bottom=img[8*q:9*q,12*q:13*q]

        rh1_right=img[5*q:8*q,10*q:11*q]
        rh2_right=img[9*q:12*q,10*q:11*q]

        rh1_left=img[5*q:8*q,12*q:13*q]
        rh2_left=img[9*q:12*q,12*q:13*q]

        rh1_back=img[5*q:8*q,13*q:14*q]
        rh2_back=img[9*q:12*q,13*q:14*q]
    else:
        rh1_front=img[5*q:8*q,11*q:12*q-1]
        rh2_front=img[9*q:12*q,11*q:12*q-1]
        rh1_top=img[4*q:5*q,11*q:12*q-1]
        rh2_top=img[8*q:9*q,11*q:12*q-1]

        rh1_bottom=img[4*q:5*q,12*q-1:13*q-2]
        rh2_bottom=img[8*q:9*q,12*q-1:13*q-2]

        rh1_right=img[5*q:8*q,10*q:11*q]
        rh2_right=img[9*q:12*q,10*q:11*q]

        rh1_left=img[5*q:8*q,12*q-1:13*q-1]
        rh2_left=img[9*q:12*q,12*q-1:13*q-1]

        rh1_back=img[5*q:8*q,13*q-1:14*q-2]
        rh2_back=img[9*q:12*q,13*q-1:14*q-2]
        


    #一回transposeしてるから逆になる
    xp=4
    if not iswide:
        xp=3
    yp=4
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    #print(x,y)
    x=x-float(xp/2.0)
    y=y-float(yp/2.0)
    Y, X = np.meshgrid(y, x)
    #print(X,Y)
    #head
    #x,y平面(上面)
    #print(Y.shape)
    #print(np.fliplr(body1_top.transpose((1,0,2))).shape)
    ax.plot_surface(X-d, Y, X-X+6+z, facecolors=np.fliplr(rh1_top.transpose((1,0,2))),
            rstride=1, cstride=1,
            antialiased=True, shade=False)
    ax.plot_surface(X*k-d, Y*k, X-X+6*k+z, facecolors=np.fliplr(rh2_top.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #底面
    ax.plot_surface(X-d, Y, X-X-6+z, facecolors=np.fliplr(rh1_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X*k-d, Y*k, X-X-6*k+z, facecolors=np.fliplr(rh2_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    xp=12
    yp=4
    if not iswide:
        yp=3
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-float(xp/2.0)
    y=y-float(yp/2.0)
    Y, X = np.meshgrid(y, x)    
    #x,z平面(正面)
    ax.plot_surface(Y-d, X-X-2, X+z, facecolors=np.flipud(rh1_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k-d, X-X-2*k, X*k+z, facecolors=np.flipud(rh2_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
        #背面
    ax.plot_surface(Y-d, X-X+2, X+z, facecolors=np.fliplr(np.flipud(rh1_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k-d, X-X+k*2, X*k+z, facecolors=np.fliplr(np.flipud(rh2_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
     #一回transposeしてるから逆になる
    xp=4
    yp=12
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-float(xp/2.0)
    y=y-float(yp/2.0)
    Y, X = np.meshgrid(y, x)    
    #y,z平面
    grid=2
    if not iswide:
        grid=1.5
    ax.plot_surface(X-X+grid-d, X, Y+z, facecolors=np.fliplr(rh1_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X+grid*k-d, X*k, Y*k+z, facecolors=np.fliplr(rh2_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #右面
    ax.plot_surface(X-X-grid-d, X, Y+z, facecolors=np.flipud(np.fliplr(rh1_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X-grid*k-d, X*k, Y*k+z, facecolors=np.flipud(np.fliplr(rh2_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
def left_hand(img,k,ax,q,iswide):
	z=14
	d=6
	if iswide:
		rh1_front=img[13*q:16*q,9*q:10*q]
		rh2_front=img[13*q:16*q,13*q:14*q]
		rh1_top=img[12*q:13*q,9*q:10*q]
		rh2_top=img[12*q:13*q,13*q:14*q]

		rh1_bottom=img[12*q:13*q,10*q:11*q]
		rh2_bottom=img[12*q:13*q,14*q:15*q]

		rh1_right=img[13*q:16*q,8*q:9*q]
		rh2_right=img[13*q:16*q,12*q:13*q]

		rh1_left=img[13*q:16*q,10*q:11*q]
		rh2_left=img[13*q:16*q,14*q:15*q]

		rh1_back=img[13*q:16*q,11*q:12*q]
		rh2_back=img[13*q:16*q,15*q:16*q]
	else:
		rh1_front=img[13*q:16*q,9*q:10*q-1]
		rh2_front=img[13*q:16*q,13*q:14*q-1]
		rh1_top=img[12*q:13*q,9*q:10*q-1]
		rh2_top=img[12*q:13*q,13*q:14*q-1]

		rh1_bottom=img[12*q:13*q,10*q-1:11*q-2]
		rh2_bottom=img[12*q:13*q,14*q-1:15*q-2]

		rh1_right=img[13*q:16*q,8*q:9*q]
		rh2_right=img[13*q:16*q,12*q:13*q]

		rh1_left=img[13*q:16*q,10*q-1:11*q-1]
		rh2_left=img[13*q:16*q,14*q-1:15*q-1]

		rh1_back=img[13*q:16*q,11*q-1:12*q-2]
		rh2_back=img[13*q:16*q,15*q-1:16*q-2]
    #一回transposeしてるから逆になる
	xp=4
	if not iswide:
		xp=3
	yp=4
	x = np.arange(0, xp+1)
	y = np.arange(0, yp+1)
	#print(x,y)
	x=x-float(xp/2.0)
	y=y-float(yp/2.0)
	Y, X = np.meshgrid(y, x)
	#print(X,Y)
	#head
	#x,y平面(上面)
	#print(Y.shape)
	#print(np.fliplr(body1_top.transpose((1,0,2))).shape)
	ax.plot_surface(X+d, Y, X-X+6+z, facecolors=np.fliplr(rh1_top.transpose((1,0,2))),
			rstride=1, cstride=1,
			antialiased=True, shade=False)
	ax.plot_surface(X*k+d, Y*k, X-X+6*k+z, facecolors=np.fliplr(rh2_top.transpose((1,0,2))),
				rstride=1, cstride=1,
				antialiased=True, shade=False)
		#底面
	ax.plot_surface(X+d, Y, X-X-6+z, facecolors=np.fliplr(rh1_bottom.transpose((1,0,2))),
				rstride=1, cstride=1,
				antialiased=True, shade=False)
	ax.plot_surface(X*k+d, Y*k, X-X-6*k+z, facecolors=np.fliplr(rh2_bottom.transpose((1,0,2))),
				rstride=1, cstride=1,
				antialiased=True, shade=False)
	xp=12
	yp=4
	if not iswide:
		yp=3
	x = np.arange(0, xp+1)
	y = np.arange(0, yp+1)
	x=x-float(xp/2.0)
	y=y-float(yp/2.0)
	Y, X = np.meshgrid(y, x)    
	#x,z平面(正面)
	ax.plot_surface(Y+d, X-X-2, X+z, facecolors=np.flipud(rh1_front),
				#rstride=1, cstride=1,
				antialiased=True, shade=False)
	ax.plot_surface(Y*k+d, X-X-2*k, X*k+z, facecolors=np.flipud(rh2_front),
				#rstride=1, cstride=1,
				antialiased=True, shade=False)
		#背面
	ax.plot_surface(Y+d, X-X+2, X+z, facecolors=np.fliplr(np.flipud(rh1_back)),
				#rstride=1, cstride=1,
				antialiased=True, shade=False)
	ax.plot_surface(Y*k+d, X-X+k*2, X*k+z, facecolors=np.fliplr(np.flipud(rh2_back)),
				#rstride=1, cstride=1,
				antialiased=True, shade=False)
		#一回transposeしてるから逆になる
	xp=4
	yp=12

	x = np.arange(0, xp+1)
	y = np.arange(0, yp+1)
	x=x-float(xp/2.0)
	y=y-float(yp/2.0)
	Y, X = np.meshgrid(y, x)    
	#y,z平面
	grid=2
	if not iswide:
		grid=1.5
	ax.plot_surface(X-X+grid+d, X, Y+z, facecolors=np.fliplr(rh1_left.transpose((1,0,2))),
				rstride=1, cstride=1,
				antialiased=True, shade=False)
	ax.plot_surface(X-X+grid*k+d, X*k, Y*k+z, facecolors=np.fliplr(rh2_left.transpose((1,0,2))),
				rstride=1, cstride=1,
				antialiased=True, shade=False)
		#右面
	ax.plot_surface(X-X-grid+d, X, Y+z, facecolors=np.flipud(np.fliplr(rh1_right.transpose((1,0,2)))),
				rstride=1, cstride=1,
				antialiased=True, shade=False)
	ax.plot_surface(X-X-grid*k+d, X*k, Y*k+z, facecolors=np.flipud(np.fliplr(rh2_right.transpose((1,0,2)))),
				rstride=1, cstride=1,
				antialiased=True, shade=False)
def right_leg(img,k,ax,q):
    z=2
    d=2
    rh1_front=img[5*q:8*q,1*q:2*q]
    rh2_front=img[9*q:12*q,1*q:2*q]
    rh1_top=img[4*q:5*q,1*q:2*q]
    rh2_top=img[8*q:9*q,1*q:2*q]

    rh1_bottom=img[4*q:5*q,2*q:3*q]
    rh2_bottom=img[8*q:9*q,2*q:3*q]

    rh1_right=img[5*q:8*q,0*q:1*q]
    rh2_right=img[9*q:12*q,0*q:1*q]

    rh1_left=img[5*q:8*q,2*q:3*q]
    rh2_left=img[9*q:12*q,2*q:3*q]

    rh1_back=img[5*q:8*q,3*q:4*q]
    rh2_back=img[9*q:12*q,3*q:4*q]
    #一回transposeしてるから逆になる
    xp=4
    yp=4
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    #print(x,y)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)
    #print(X,Y)
    #head
    #x,y平面(上面)
    #print(Y.shape)
    #print(np.fliplr(body1_top.transpose((1,0,2))).shape)
    ax.plot_surface(X-d, Y, X-X+6+z, facecolors=np.fliplr(rh1_top.transpose((1,0,2))),
            rstride=1, cstride=1,
            antialiased=True, shade=False)
    ax.plot_surface(X*k-d, Y*k, X-X+6*k+z, facecolors=np.fliplr(rh2_top.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #底面
    ax.plot_surface(X-d, Y, X-X-6+z, facecolors=np.fliplr(rh1_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X*k-d, Y*k, X-X-6*k+z, facecolors=np.fliplr(rh2_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    xp=12
    yp=4
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)    
    #x,z平面(正面)
    ax.plot_surface(Y-d, X-X-2, X+z, facecolors=np.flipud(rh1_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k-d, X-X-2*k, X*k+z, facecolors=np.flipud(rh2_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
        #背面
    ax.plot_surface(Y-d, X-X+2, X+z, facecolors=np.fliplr(np.flipud(rh1_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k-d, X-X+k*2, X*k+z, facecolors=np.fliplr(np.flipud(rh2_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
     #一回transposeしてるから逆になる
    xp=4
    yp=12
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)    
    #y,z平面
    ax.plot_surface(X-X+2-d, X, Y+z, facecolors=np.fliplr(rh1_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X+2*k-d, X*k, Y*k+z, facecolors=np.fliplr(rh2_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #右面
    ax.plot_surface(X-X-2-d, X, Y+z, facecolors=np.flipud(np.fliplr(rh1_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X-2*k-d, X*k, Y*k+z, facecolors=np.flipud(np.fliplr(rh2_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
def left_leg(img,k,ax,q):
    z=2
    d=2
    rh2_front=img[13*q:16*q,1*q:2*q]
    rh1_front=img[13*q:16*q,5*q:6*q]
    rh2_top=img[12*q:13*q,1*q:2*q]
    rh1_top=img[12*q:13*q,5*q:6*q]

    rh2_bottom=img[12*q:13*q,2*q:3*q]
    rh1_bottom=img[12*q:13*q,6*q:7*q]

    rh2_right=img[13*q:16*q,0*q:1*q]
    rh1_right=img[13*q:16*q,4*q:5*q]

    rh2_left=img[13*q:16*q,2*q:3*q]
    rh1_left=img[13*q:16*q,6*q:7*q]

    rh2_back=img[13*q:16*q,3*q:4*q]
    rh1_back=img[13*q:16*q,7*q:8*q]
    #一回transposeしてるから逆になる
    xp=4
    yp=4
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    #print(x,y)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)
    #print(X,Y)
    #head
    #x,y平面(上面)
    #print(Y.shape)
    #print(np.fliplr(body1_top.transpose((1,0,2))).shape)
    ax.plot_surface(X+d, Y, X-X+6+z, facecolors=np.fliplr(rh1_top.transpose((1,0,2))),
            rstride=1, cstride=1,
            antialiased=True, shade=False)
    ax.plot_surface(X*k+d, Y*k, X-X+6*k+z, facecolors=np.fliplr(rh2_top.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #底面
    ax.plot_surface(X+d, Y, X-X-6+z, facecolors=np.fliplr(rh1_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X*k+d, Y*k, X-X-6*k+z, facecolors=np.fliplr(rh2_bottom.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    xp=12
    yp=4
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)    
    #x,z平面(正面)
    ax.plot_surface(Y+d, X-X-2, X+z, facecolors=np.flipud(rh1_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k+d, X-X-2*k, X*k+z, facecolors=np.flipud(rh2_front),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
        #背面
    ax.plot_surface(Y+d, X-X+2, X+z, facecolors=np.fliplr(np.flipud(rh1_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(Y*k+d, X-X+k*2, X*k+z, facecolors=np.fliplr(np.flipud(rh2_back)),
                #rstride=1, cstride=1,
                antialiased=True, shade=False)
     #一回transposeしてるから逆になる
    xp=4
    yp=12
    x = np.arange(0, xp+1)
    y = np.arange(0, yp+1)
    x=x-int(xp/2)
    y=y-int(yp/2)
    Y, X = np.meshgrid(y, x)    
    #y,z平面
    ax.plot_surface(X-X+2+d, X, Y+z, facecolors=np.fliplr(rh1_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X+2*k+d, X*k, Y*k+z, facecolors=np.fliplr(rh2_left.transpose((1,0,2))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
        #右面
    ax.plot_surface(X-X-2+d, X, Y+z, facecolors=np.flipud(np.fliplr(rh1_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)
    ax.plot_surface(X-X-2*k+d, X*k, Y*k+z, facecolors=np.flipud(np.fliplr(rh2_right.transpose((1,0,2)))),
                rstride=1, cstride=1,
                antialiased=True, shade=False)

def main(ax,img,iswide):
    p,q=(8,4)
    k=pow(1.5,1/2)
    k2=pow(1.25,1/2)

    head(img,k,ax,p)
    body(img,k2,ax,q)
    right_hand(img,k2,ax,q,iswide)
    left_hand(img,k2,ax,q,iswide)
    right_leg(img,k2,ax,q)
    left_leg(img,k2,ax,q)

    l=10
    plt.xlim([-l,l])
    plt.ylim([-l,l])
    ax.set_zlim(32-4*l,32)
    #plt.show()
    #fig.savefig("img.png",transparent=True,dpi=300)
if __name__=="__main__":
    img = image.imread('MCskin/yoshi_kyou_sinja.png')
    plt.clf()
    plt.close()
    p,q=(8,4)
    k=pow(1.5,1/2)
    k2=pow(1.25,1/2)
    #print(k)


    fig = plt.figure(figsize=(4,7))
    ax = fig.add_subplot(111, projection='3d')
    head(img,k,ax,p)
    body(img,k2,ax,q)
    right_hand(img,k2,ax,q)
    left_hand(img,k2,ax,q)

    right_leg(img,k2,ax,q)
    left_leg(img,k2,ax,q)

    ax.axis("off")
    ax.set_box_aspect((1,1,2))
    l=10
    plt.xlim([-l,l])
    plt.ylim([-l,l])
    ax.set_zlim(32-4*l,32)
    plt.show()
    fig.savefig("img.png",transparent=True,dpi=300)