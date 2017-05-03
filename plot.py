import flint
import mpmath
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pylab
import matplotlib.patches as mpatches
from numpy import arange
from flint import arb, acb

legends = []

plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

def ploterr(ax, f, xab, yab, step, yrange=None, color=None, label=None, hatch=None, alpha=1.0):
    print "yah"
    xrad = step * 0.5
    a, b = xab
    top = 0.0
    bot = 0.0
    for xx in arange(a,b,2*xrad):
        xmid = xx + xrad
        X = arb(xmid, xrad)
        if abs(xmid + xrad) < 1e-10:
            X = -((-X).nonnegative_part())
        elif abs(xmid - xrad) < 1e-10:
            X = X.nonnegative_part()
        Y = f(X)
        if Y.is_finite():
            ymid = float(arb(Y.mid()))
            yrad = float(arb(Y.rad()))
            top = max(top, (ymid + yrad) * 1.2)
            bot = min(bot, (ymid - yrad) * 1.2)
            ax.add_patch(patches.Rectangle((xmid-xrad, ymid-yrad), 2*xrad, 2*yrad, color=color, alpha=alpha, hatch=hatch))
        else:
            ax.add_patch(patches.Rectangle((xmid-xrad, -1e50), 2*xrad, 1e50, color=color, alpha=alpha, hatch=hatch))
    ax.set_xlim([a,b])
    if yab is None:
        ax.set_ylim([bot,top])
    else:
        ax.set_ylim(yab)
    if label is None:
        label = 'Step %s' % step
    patch1 = mpatches.Patch(color=color, label=label, alpha=alpha, hatch=hatch)
    legends.append(patch1)

def plotadaptive(ax, f, xab, yab, goal=0.1, yrange=None, color=None, label=None, hatch=None, alpha=1.0):
    queue = [arb(0.5*(xab[0]+xab[1]), 0.5*(xab[1]-xab[0]))]
    top = 0.0
    bot = 0.0
    while queue:
        X = queue.pop()
        Y = f(X)
        xmid = float(arb(X.mid()))
        xrad = float(arb(X.rad()))
        ymid = float(arb(Y.mid()))
        yrad = float(arb(Y.rad()))
        if yrad < goal:
            top = max(top, (ymid + yrad) * 1.2)
            bot = min(bot, (ymid - yrad) * 1.2)
            ax.add_patch(patches.Rectangle((xmid-xrad, ymid-yrad), 2*xrad, 2*yrad, color=color, alpha=alpha, hatch=hatch))
        elif xrad > goal*0.001:
            xa = arb(xmid-xrad*0.5, xrad*0.5)
            xb = arb(xmid+xrad*0.5, xrad*0.5)
            queue += [xa, xb]
            #ax.add_patch(patches.Rectangle((xmid-xrad, -1e50), 2*xrad, 1e50, color=color, alpha=alpha, hatch=hatch))
    ax.set_xlim([xab[0],xab[1]])
    if yab is None:
        ax.set_ylim([bot,top])
    else:
        ax.set_ylim(yab)
    patch1 = mpatches.Patch(color=color, label=label, alpha=alpha, hatch=hatch)
    legends.append(patch1)

def figure1():
    global legends
    plt.clf()
    ax = plt.gca()
    legends = []
    ax.grid(True)
    R = float(-arb(-1).exp())

    k = 0
    plotadaptive(ax, lambda X: acb(X).lambertw(k).real, [R, 3], [-3,2], 0.5, color="lightblue", label="$W_{0}(x), \\varepsilon = 0.5$", alpha=0.6)
    plotadaptive(ax, lambda X: acb(X).lambertw(k).real, [R, 3], [-3,2], 0.1, color="blue", label="$W_{0}(x), \\varepsilon = 0.1$", alpha=0.7)
    plotadaptive(ax, lambda X: acb(X).lambertw(k).real, [R, 3], [-3,2], 0.01, color="black", label="$W_{0}(x), \\varepsilon = 0.01$", alpha=1.0)

    k = -1
    plotadaptive(ax, lambda X: acb(X).lambertw(k).real, [R, 0], [-3,2], 0.5, color="orange", label="$W_{-1}(x), \\varepsilon = 0.5$", alpha=0.4)
    plotadaptive(ax, lambda X: acb(X).lambertw(k).real, [R, 0], [-3,2], 0.1, color="red", label="$W_{-1}(x), \\varepsilon = 0.1$", alpha=0.8)
    #plotadaptive(ax, lambda X: acb(X).lambertw(k).real, [R, 0], [-3,2], 0.01, color="black", label="$W_{-1}(x), \\varepsilon = 0.01$", alpha=1.0)

    ax.set_xlim([-1,3])
    ax.set_ylim([-4,2])
    ax.axhline(y=-1, color="gray")
    ax.axvline(x=R, color="gray")

    plt.xticks([-1, R, 0, 1, 2, 3], ["$-1$", "$-1/e$", "$0$", "$1$", "$2$", "$3$"])
    plt.xlabel("$x$")
    plt.ylabel("$W_k(x)$")
    ax.legend(handles=legends, loc="best")
    import matplotlib
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8, 5)
    fig.savefig('test1aa.png', bbox_inches="tight")
    fig.savefig('branchplot1.pdf', bbox_inches="tight")


def figure2():
    global legends
    plt.clf()
    ax = plt.gca()
    legends = []
    ax.grid(True)
    k = 1
    #R = -arb(-1).exp()
    R = -1
    ploterr(ax, lambda X: acb(R,X).lambertw(k).real, [-3, 3], [-3,1], 0.5, color="lightblue", label="$h = 0.5$", alpha=0.7)
    ploterr(ax, lambda X: acb(R,X).lambertw(k).real, [-3, 3], [-3,1], 0.1, color="blue", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda X: acb(R,X).lambertw(k).real, [-3, 3], [-3,1], 0.02, color="black", label="$h = 0.02$", alpha=1.0)
    plt.xlabel("$y$")
    plt.ylabel("$\Re(W_{%ld}(-1+yi))$" % k)
    ax.legend(handles=legends, loc="best")
    import matplotlib
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8, 5)
    fig.savefig('test2.png', bbox_inches="tight")
    fig.savefig('branchplot2.pdf', bbox_inches="tight")

def figure3():
    global legends
    plt.clf()
    ax = plt.gca()
    legends = []
    ax.grid(True)
    k = 1
    R = -arb(-1).exp()
    ploterr(ax, lambda X: acb(R,X).lambertw(k).real, [-4, 4], [-5,1], 0.5, color="lightblue", label="$h = 0.5$", alpha=0.7)
    ploterr(ax, lambda X: acb(R,X).lambertw(k).real, [-4, 4], [-5,1], 0.1, color="blue", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda X: acb(R,X).lambertw(k).real, [-4, 4], [-5,1], 0.01, color="black", label="$h = 0.01$", alpha=1.0)
    plt.xlabel("$y$")
    plt.ylabel("$\Re(W_{%ld}(-1/e+yi))$" % k)
    ax.legend(handles=legends, loc="upper right")
    import matplotlib
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8, 5)
    fig.savefig('test2.png', bbox_inches="tight")
    fig.savefig('branchplot2.pdf', bbox_inches="tight")

def spiral():
    global legends
    plt.clf()
    ax = plt.gca()
    legends = []
    ax.grid(True)
    R = -arb(-1).exp()
    yrange = [-5,15]
    h = 1/13.
    if 1:
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(0).imag, [-0.5, 0.5], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(0, flags=2).imag, [0.5, 1.5], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(1).imag, [1.5, 2.5], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(1, flags=2).imag, [2.5, 3.5], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(2).imag, [3.5, 4.5], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(2, flags=2).imag, [4.5, 5.5], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)

        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(0).real, [-0.5, 0.5], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(0, flags=2).real, [0.5, 1.5], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(1).real, [1.5, 2.5], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(1, flags=2).real, [2.5, 3.5], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(2).real, [3.5, 4.5], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
        ploterr(ax, lambda X: acb(X).exp_pi_i().lambertw(2, flags=2).real, [4.5, 5.5], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)

        ax.set_xlim([-0.5,5.5])

    else:
        print "zagurra"
        ploterr(ax, lambda X: (acb(X)+acb(1-X**2).sqrt()*1j).lambertw(0).imag, [0.0, 1.0], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
        print "zagurra1"
        ploterr(ax, lambda X: (acb(X)+acb(1-X**2).sqrt()*1j).lambertw(0, flags=2).imag, [-1.0, 0.0], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
        print "zagurra2"
        ploterr(ax, lambda X: (acb(X)-acb(1-X**2).sqrt()*1j).lambertw(0, flags=2).imag, [-1.0, 0.0], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
        print "zagurra3"
        ploterr(ax, lambda X: (acb(X)-acb(1-X**2).sqrt()*1j).lambertw(1).imag, [0.0, 1.0], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)

        ax.set_xlim([-1.5,1.5])
        ax.set_ylim([-5,5])


    plt.xlabel("$\\theta$")
    plt.ylabel("$W(e^{\\pi i \\theta})$")
    #ax.legend(handles=legends, loc="upper right")
    import matplotlib
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8, 5)
    fig.savefig('tests.png', bbox_inches="tight")
    fig.savefig('branchplots.pdf', bbox_inches="tight")


def spiralb():
    global legends
    plt.clf()
    ax = plt.gca()
    legends = []
    ax.grid(True)
    R = -arb(-1).exp()
    yrange = [-2,2]

    #def G(z, k):
    #    return lambertw((z**2/(2*e))-1/e,k)

    #def H(x, k):
    #    return abs(1+G(exp(pi*1j*x), k))

    #plot([lambda x: H(x, 0), lambda x: H(x, 1), lambda x: H(x, -1)], [0, 2], [0,2])

    #0   to 0.5   0
    #0.5 to 1     1
    #1   to 1.5  -1
    #1.5 to 2.0   0

    indet = acb("+/- inf", "+/- inf")

    def B(t):
        Z2 = (1.25 * 1.25) * acb(2*t).exp_pi_i()
        Z = (Z2-2)/(2*acb(1).exp())
        t = float(t)
        print t
        if t < 0.25:
            W = Z.lambertw()
        elif t < 0.75:
            W = Z.lambertw(branch=0,flags=2)
        elif t < 0.9:
            W = Z.lambertw(branch=1)
        elif t < 1.1:
            W = Z.lambertw(branch=-1,flags=4)
        elif t < 1.25:
            W = Z.lambertw(branch=-1)
        elif t < 1.75:
            W = Z.lambertw(branch=-1,flags=2)
        else:
            W = Z.lambertw()
        res = 2 + W
        if not abs(res) < 2:
            return indet
        #    raise ValueError
        return res

    plotadaptive(ax, lambda z: B(z).real, [0.0, 2.0], yrange, goal=0.1, color="blue", alpha=0.5)
    plotadaptive(ax, lambda z: B(z).imag, [0.0, 2.0], yrange, goal=0.1, color="red", alpha=0.5)
    plotadaptive(ax, lambda z: abs(B(z)), [0.0, 2.0], yrange, goal=0.1, color="black", alpha=0.5)


    """
    h = 1 / 64.
    ploterr(ax, lambda z: B(z).real, [0.0, 0.75], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda z: B(z).imag, [0.0, 0.75], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda z: abs(B(z)), [0.0, 0.75], yrange, h, color="black", label="$h = 0.1$", alpha=0.5)

    h = 1 / 512.
    ploterr(ax, lambda z: B(z).real, [0.75, 1.25], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda z: B(z).imag, [0.75, 1.25], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda z: abs(B(z)), [0.75, 1.25], yrange, h, color="black", label="$h = 0.1$", alpha=0.5)

    h = 1 / 64.
    ploterr(ax, lambda z: B(z).real, [1.25, 2.0], yrange, h, color="blue", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda z: B(z).imag, [1.25, 2.0], yrange, h, color="red", label="$h = 0.1$", alpha=0.5)
    ploterr(ax, lambda z: abs(B(z)), [1.25, 2.0], yrange, h, color="black", label="$h = 0.1$", alpha=0.5)
    """

    ax.set_xlim([0.0,2.0])
    ax.set_ylim([-2.0,3.0])

    plt.xlabel("$\\theta$")
    plt.ylabel("$W((z^2-2)/(2e)), z = 1.25 e^{\\pi i \\theta}$")
    #ax.legend(handles=legends, loc="upper right")
    import matplotlib
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8, 5)
    fig.savefig('testb.png', bbox_inches="tight")
    fig.savefig('branchplotb.pdf', bbox_inches="tight")


#figure1()
#figure3()


#figure2()
#spiral()
spiralb()

