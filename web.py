import streamlit as st
from streamlit import caching
from streamlit_ace import st_ace
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as rd
import pandas as pd
import statsmodels.formula.api as smf

from scipy.stats import norm, binom, t, multivariate_normal
from io import BytesIO
from exbook import book as eb

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA


def main():
    st.title('Programming for Business Analytics')
    subtitle = '### Department of Analytics & Operations, NUS Business School'
    st.markdown(subtitle)

    topics = ['About',
              'Functions, Modules, and Packages',
              'Review of Probability Theory',
              'Sampling Distributions',
              'Confidence Intervals and Hypothesis Testing',
              'Explanatory Modeling: Regression',
              'Predictive Modeling: Regression',
              'Predictive Modeling: Classification']

    topic = st.selectbox('Select a topic: ', topics)

    if topic == topics[0]:
        about()
    elif topic == topics[1]:
        exbook_web()
    elif topic == topics[2]:
        prob_review()
    elif topic == topics[3]:
        samp_distr()
    elif topic == topics[4]:
        conf_int()
    elif topic == topics[5]:
        exp_regress()
    elif topic == topics[6]:
        pred_regress()
        reduce_dim()
        pca_vis()
    elif topic == topics[7]:
        pred_class()


def about():

    st.components.v1.html("""<a href="https://github.com/XiongPengNUS/learn_dao" target="_blank"><img src="https://img.shields.io/static/v1?label=XiongPengNUS&message=learn_dao&color=blue&logo=github" alt="XiongPengNUS - learn_dao"></a>
<a href="https://github.com/XiongPengNUS/learn_dao" target="_blank"><img src="https://img.shields.io/github/stars/XiongPengNUS/learn_dao?style=social" alt="stars - learn_dao"></a>""", height=28)

    st.markdown("---")
    st.markdown("This web application is a learning tool used for NUS modules: ")
    st.markdown("- [**DAO2702 Programming for Business Analytics**](https://nusmods.com/modules/DAO2702/programming-for-business-analytics)")
    st.markdown("- [**BMK5202 Python Programming for Business Analytics**](https://nusmods.com/modules/BMK5202/python-programming-for-business-analytics) ")

    st.markdown("""You may use the app to access interactive coding practice questions and
    visualizations that illustrate the concepts of statistics and regression analysis. """)

    st.markdown("**Author**: [Peng Xiong](https://bizfaculty.nus.edu.sg/faculty-details/?profId=543)")


def exbook_web():

    def check(question, func, cheat):
        correct = []
        keys = ['Input '+str(i+1) + ': ' + type(question._Question__inputs[0][i]).__name__
                for i in range(len(question._Question__inputs[0]))] + \
               ['Your output'] + \
               ['Correct output: ' + type(question._Question__outputs[0][0]).__name__] + \
               ['Correct']
        cheat_dict = {key: [] for key in keys}
        cheat_table = pd.DataFrame(cheat_dict)
        for each_input, each_output in zip(question._Question__inputs, question._Question__outputs):
            arg_string = ''
            cheat_list = []
            for n in range(len(each_input)):
                if isinstance(each_input[n], (list, dict)):
                    arg_string += 'deepcopy(each_input[{0:d}])'.format(n)
                else:
                    arg_string += 'each_input[{0:d}]'.format(n)
                if n < len(each_input) - 1:
                    arg_string = arg_string + ', '
                cheat_list.append(str(each_input[n]))
            this_output = eval('func(' + arg_string + ')')
            if question.compset:
                if set(this_output) == set(each_output[0]):
                    correct.append(True)
                else:
                    correct.append(False)
            else:
                if this_output == each_output[0]:
                    correct.append(True)
                else:
                    correct.append(False)
            cheat_list = cheat_list + [str(this_output),
                                       str(each_output[0]),
                                       str(correct[-1])]
            test_dict = {keys[i]: cheat_list[i]
                         for i in range(len(keys))}
            cheat_table = cheat_table.append(test_dict, ignore_index=True)

        if cheat:
            cheat_table.rename(index={i: 'Test {0}:'.format(i+1)
                                      for i in range(cheat_table.shape[0])},
                                      inplace=True)
            st.write(cheat_table)

        correctness = 'incorrect' if False in correct else 'correct'
        right_ones = sum(correct)
        st.markdown('### Test results: ')
        st.markdown('You passed {0} of the {1} tests. \n'
                    'The solution is {2}'.format(right_ones,
                                                 len(correct), correctness))
        if correctness == 'correct':
            st.balloons()

    st.markdown('---')
    st.markdown("""This is the web version of the `exbook` package. It provides a set of coding practice questions, and your solutions
    are marked automatically by a number of tests.""")
    st.components.v1.html("""<a href="https://github.com/XiongPengNUS/exbook" target="_blank"><img src="https://img.shields.io/static/v1?label=XiongPengNUS&message=exbook&color=blue&logo=github" alt="XiongPengNUS - exbook"></a>
<a href="https://github.com/XiongPengNUS/exbook" target="_blank"><img src="https://img.shields.io/github/stars/XiongPengNUS/exbook?style=social" alt="stars - exbook"></a>""", height=28)
    st.markdown('---')

    ids = ['{}. {} ({})'.format(index, ex.id, ex.level) for index, ex in zip(range(1, len(eb)+1), eb)]

    label = st.selectbox('Select a question', ids)
    index = int(label[:label.find('.')])
    question = eb[index-1]

    all_inputs = question._Question__inputs
    keys = ['Input' + str(i+1) +
            ': ' + type(all_inputs[0][i]).__name__
            for i in range(len(all_inputs[0]))] + \
            ['Output: ' + type(question._Question__outputs[0][0]).__name__]
    cheat_dict = {key: [] for key in keys}
    cheat_table = pd.DataFrame(cheat_dict)
    for i in question.index:
        cheat_list = []
        each_input = question._Question__inputs[i]
        each_output = question._Question__outputs[i]
        for n in range(len(each_input)):
            cheat_list.append(str(each_input[n]))
        cheat_list = cheat_list + [str(each_output[0])]
        sample_dict = {keys[j]: cheat_list[j]
                       for j in range(len(keys))}
        cheat_table = cheat_table.append(sample_dict, ignore_index=True)

    cheat_table.rename(index={i: 'Test {0}:'.format(i+1)
                              for i in range(cheat_table.shape[0])},
                              inplace=True)

    st.write(question._Question__readme)
    st.write(cheat_table)

    fun_name = st.text_input('Name of the function to be tested: ')
    cheat = st.checkbox('Cheat table')
    st.markdown('<p style="font-size: 13px;">Definition of the function:</p>', unsafe_allow_html=True)
    solution = st_ace(language='python')

    if solution != '' and fun_name != '':
        try:
            exec(solution)
            exec('check(question, {}, cheat)'.format(fun_name))
        except Exception as e:
            st.markdown('### Error!')
            st.markdown(str(e))

def prob_review():

    st.markdown('---')
    st.header('Discrete Random Variable')
    st.markdown(r"""A random variable $X$ is defined to be **discrete** if its possible
    outcomes are finite or countable. Examples of distributions of discrete random
    variables are discrete uniform distribution (*i.e.*, outcome of rolling an even die),
    Bernoulli distribution (*i.e.*, the preference of a randomly selected customer for
    Coke or Pepsi), Binomial distribution (*i.e.*, the number of customers who prefer
    Coke over Pepsi among 10 randomly selected customers), and Poisson distribution
    (*i.e.*, The number of patients arriving in an emergency room within a fixed time
    interval) etc. """)
    st.error("""**Notes**: For a discrete random variable $X$ with $k$ possible outcomes
    $x_j$, \n- the **probability mass function (PMF)** is given by: $P(X=x_j) = p_j$, for
    each $j=1, 2, ..., k$, where $p_j$ is the probability of the outcome $x_j$, and all
    $p_i$ must satisfy \n
    $$
    \\begin{cases} 0\\leq p_i \leq 1 \\\\
    \\sum_{j=1}^kp_j = 1
    \\end{cases}
    $$
    \n- The **cumulative distribution function (CDF)** of a random variable
    $X$ is defined as $F(x) = P(X\leq x)$.""")
    st.markdown("""Suppose that in Singapore, the proportion of customers who prefer Coke
    is $p$, and the remaining $p-1$ of all customers prefer Pepsi. Now we randomly survey
    $n$ customers, among which the number of customers who prefer Coke is denoted by a
    discrete random variable $X$. The PMF of $X$ and its CDF are illustrated by the graph
    below.""")

    binom_visual()

    st.markdown('---')
    st.header('Continuous Random Variables')
    st.markdown("""A variable $X$ is a **continuous random variable** if it takes on
    any real value with *zero* probability. Random variables following uniform, normal
    (Gaussian) and exponential distributions are all continuous variables.""")
    st.markdown("""For continuous random variables, there is no PMF as the discrete
    random variables, because $P(X=x)=0$ for all values of $x$. The CDF for a continuous
    random variable has the same definition as the discrete case, which is $F(x)=P(X\leq x)$.
    Based on the CDF, we have other definitions listed as follows.""")

    st.error("""**Notes**: Let $F(x)$ be the CDF of a continuous random variable $X$,
    then \n- The derivative $f(x) = \\frac{\\text{d} F(x)}{\\text{d}x}$ of the CDF $F(x)$
    is called the **probability density function (PDF)** of $X$. This definition also
    implies that $F(x) = \int_{-\infty}^{x}f(t)dt$. \n- The inverse of CDF $F(x)$, denoted
    by $F^{-1}(q)$, is called the **percent point function (PPF)**, where $q$ is the given
    cumulative probability. This function is sometimes referred to as the **inverse
    distribution function** or the **quantile function**.""")

    st.markdown("""The distribution diagram below is used to illustrate the concepts of PDF,
    CDF, and PPF. """)

    normal_visual()


def binom_visual():

    p = st.slider('Proportion of all customers who prefer Coke: ',
                  min_value=0.1, max_value=0.9, value=0.4, step=0.05)
    n = st.slider('Number of surveyed customers: ',
                  min_value=5, max_value=100, value=15, step=5)
    m = st.slider('Among the surveyed customers, the number of them who prefer Coke: ',
                  min_value=0.0, max_value=float(n), value=float(n//2),
                  step=0.1 if n <= 10 else 0.2 if n <= 25 else 0.5)

    xi = np.arange(n+1)
    pi = binom.pmf(xi, n, p)
    pc = binom.cdf(xi, n, p)
    xc = list(np.array([xi[:-1], xi[1:]]).T.reshape(2*n)) + [n]
    yc = list(np.array([pc[:-1], pc[:-1]]).T.reshape(2*n)) + [1]
    ym = binom.pmf(m, n, p)
    ycm = binom.cdf(m, n, p)
    fig, ax = plt.subplots(2, 1, figsize=(7.5, 7.5))
    ax[0].vlines(xi[xi <= m], ymin=0, ymax=pi[xi <= m],
                 linewidth=3, alpha=0.5, color='b', label='Probability counted for CDF')
    ax[0].vlines(xi[xi > m], ymin=0, ymax=pi[xi > m],
                 linewidth=3, alpha=0.5, color='k', label='Probability not counted for CDF')
    ax[0].vlines(m, ymin=0, ymax=ym,
                 linewidth=3, alpha=0.5, color='r', linestyle='--')
    ax[0].scatter(m, ym, s=60, color='r', alpha=0.5)
    if p <= 0.5:
        xt, yt = n*0.7, binom.pmf(round(n*p), n, p)*0.7
        ax[0].text(xt*1.02, yt*0.99, '$P(X={0})={1:0.4f}$'.format(m, ym),
                   color='r', fontsize=12)
        if m < xt:
            ax[0].plot([m, xt], [ym, yt], linewidth=2, color='r', alpha=0.5)
        else:
            ax[0].plot([m, m], [ym, yt*0.95], linewidth=2, color='r', alpha=0.5)

        ax[0].legend(loc='upper right')
    else:
        xt, yt = n*0.3, binom.pmf(round(n*p), n, p)*0.7
        ax[0].text(-0.1*xt, yt*0.99, '$P(X={0})={1:0.4f}$'.format(m, ym),
                   color='r', fontsize=12)
        if m > xt:
            ax[0].plot([m, xt], [ym, yt], linewidth=2, color='r', alpha=0.5)
        else:
            ax[0].plot([m, m], [ym, yt*0.95], linewidth=2, color='r', alpha=0.5)

        ax[0].legend(loc='upper left')
    ax[0].set_ylabel('PMF', fontsize=12)
    ax[0].grid(True)

    ax[1].plot(xc, yc, linewidth=3, alpha=0.5, color='b', label='CDF')
    ax[1].vlines(m, ymin=0, ymax=ycm,
                 linewidth=3, alpha=0.5, color='r', linestyle='--')
    ax[1].scatter(m, ycm, s=60, color='r', alpha=0.5)
    if p <= 0.5:
        xt, yt = n*0.7, 0.7
        ax[1].text(xt*1.02, yt*0.99, '$P(X\leq{0})={1:0.4f}$'.format(m, ycm),
                   color='r', fontsize=12)
        if m < xt:
            ax[1].plot([m, xt], [ycm, yt], linewidth=2, color='r', alpha=0.5)
        else:
            ax[1].plot([m, m], [ym, yt*1.07], linewidth=2, color='r', alpha=0.5)
    else:
        xt, yt = n*0.3, 0.7
        ax[1].text(-0.1*xt, yt*0.99, '$P(X\leq{0})={1:0.4f}$'.format(m, ycm),
                   color='r', fontsize=12)
        if m > xt:
            ax[1].plot([m, xt], [ym, yt], linewidth=2, color='r', alpha=0.5)
        else:
            ax[1].plot([m, m], [ym, yt*0.95], linewidth=2, color='r', alpha=0.5)
    ax[1].set_ylabel('CDF', fontsize=12)
    ax[1].set_xlabel('Value $x$', fontsize=12)
    ax[1].grid(True)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    tx = '- `binom.pmf({}, {}, {})'.format(m, n, p)
    tx += ' = {0:6.3f}` \n'.format(binom.pmf(m, n, p))
    tx += '- `binom.cdf({}, {}, {})'.format(m, n, p)
    tx += ' = {0:6.3f}` \n'.format(binom.cdf(m, n, p))

    st.info(tx)


def normal_visual():

    st.markdown('---')
    x = st.slider('Value of the random variable:',
                  min_value=-3.5, max_value=3.5, value=-1.0, step=0.1)
    step = 0.01
    xs = np.arange(-3.6, 3.6+step, step)
    ys = norm.pdf(xs)
    xc = np.arange(-3.5, x+step, step)
    yc = norm.pdf(xc)

    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(xs, ys, color='k', linewidth=3, alpha=0.5, label='PDF curve')
    ax.fill_between(xc, y1=yc, y2=0, color='b', alpha=0.5, label='CDF')
    ax.scatter(x, 0, c='r', s=60, alpha=0.5, label='Random varaible value')

    ax.plot([x, 3], [0.5*norm.pdf(x), 0.35],
            c='b', linewidth=2.5, alpha=0.4)
    ax.plot([max(-3.6, x-0.8), x-0.01],
            [max(0.04, norm.pdf(x)), norm.pdf(x)],
            c='k', linewidth=2.5, alpha=0.5)

    ax.text(x+0.2, -0.01, '$x=$' + '{0:4.2f}'.format(x), c='r', fontsize=11)
    ax.text(1.8, 0.38, '$P(X\leq$x$)=$' + '{0:0.3f}'.format(norm.cdf(x)),
            c='b', fontsize=11)
    ax.text(max(-4.5, x-1.8), max(0.04, norm.pdf(x)-0.01), '{0:0.3f}'.format(norm.pdf(x)),
             fontsize=12)

    ax.set_xticks(np.arange(-4, 5, 1))
    ax.legend(fontsize=12, loc='upper left')
    ax.grid(True)
    ax.set_xlabel('Value $x$', fontsize=12)
    ax.set_ylabel('Probability density function', fontsize=12)
    ax.set_ylim([-0.04, 0.62])
    ax.set_xlim([-5.2, 5.2])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    tx = '- `norm.pdf({0:6.3f}, loc=0, scale=1)'.format(x)
    tx += ' = {0:6.3f}` \n'.format(norm.pdf(x))
    tx += '- `norm.cdf({0:6.3f}, loc=0, scale=1)'.format(x)
    tx += ' = {0:6.3f}` \n'.format(norm.cdf(x))
    tx += '- `norm.ppf({0:6.3f}, loc=0, scale=1)'.format(norm.cdf(x))
    tx += ' = {0:6.3f}`'.format(x)

    st.info(tx)

# @st.cache
def samp_distr():

    st.markdown('---')
    st.header('Histogram and Q-Q Plot')
    st.markdown("""Before we explore the features of the sampling distribution, we will
    introduce the graphical ways of identifying the distribution of sample data: the **histogram**,
    as a direct method that shows the shape of the sample data distribution by organizing a group of
    data points into user-specified bins (intervals); and the **Q-Q plot (quantile-quantile plot)**,
    where the sorted values of data points are compared with the quantiles of a probability distribution.
    """)
    st.markdown("""In the following example, a sample dataset is generated following the
    standard normal distribution. The histogram has a typical bell-shape, and data points in the Q-Q plot
    are linearly distributed, so the graphs could be used as evidence of normally distributed data.
    """)

    norm_id()

    st.markdown('---')
    st.header('Distribution of the Sample Mean')
    st.markdown("""Let $\{x_1, x_2, ..., x_n\}$ be a random sample of size $n$, *i.e.*, a sequence of **independent
    and identically distributed (i.i.d.)** random variables drawn from a population with an expected value $\mu$ and
    finite variance $\sigma^2$, the **sample mean** is expressed as $\\bar{x}=\\frac{1}{n}\sum_{i=1}^nx_i$.
    """)
    st.markdown("""In order to explore the distribution of the sample mean $\\bar{x}$, we conduct experiments of
    drawing random samples of size $n$ from a given population with different distributions. Such experiments are
    repeated for 1000 times to provide a rough picture of the distribution of $\\bar{x}$. """)

    samp_distr_id()

    st.markdown('---')
    st.header('Central Limit Theorem')
    st.markdown("""The experiments above show that though the distribution of the population may be greatly different
    from the normal distribution (two diagrams at the top), the sample mean would approximately follow a normal
    distribution (two diagrams at the bottom) if the sample size is sufficiently large. This is the Central limit Theorem.
    """)
    st.error("""**Central Limit Theorem (CLT)**: For a relatively large sample size, the random variable
    $\\bar{x}=\\frac{1}{n}\sum_{i=1}^nx_i$ is approximately normally distributed, regardless of the distribution of
    the population. The approximation becomes better with increased sample size.
    """)


def norm_id():

    ns = st.slider('Sample size:',
                   min_value=30, max_value=500, value=200, step=10)
    xn = rd.normal(0, 1, ns)
    bins = st.slider('Number of bins:',
                     min_value=5,
                     max_value=min(round(ns/100)*20, 30),
                     value=10, step=1 if ns <= 500 else 5)
    xn.sort()

    fig, ax = plt.subplots(1, 2, figsize=(9, 4.5))
    ax[0].hist(xn, bins, color='blue', alpha=0.5)
    ax[0].set_title('Histogram', fontsize=12)
    ax[0].set_xlabel('Sample data values', fontsize=12)
    ax[0].set_ylabel('Frequency', fontsize=12)
    ax[1].plot([-3, 3], [-3, 3], color='r', linewidth=2)
    ax[1].scatter(norm.ppf((np.arange(ns)+0.5) / ns), xn, color='b', alpha=0.3)
    ax[1].set_xlabel('Standard normal quantiles', fontsize=12)
    ax[1].set_ylabel('Ordered values', fontsize=12)
    ax[1].set_title('Q-Q plot')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)


def samp_distr_id():

    distr_list = ['Uniform distribution between 0 and 1',
                  'Exponential distribution with mean value to be 1',
                  'Standard normal distribution',
                  'Discrete uniform distribution of tossing a fair dice',
                  'Bernoulli distribution with the probability to be 0.5']
    distr = st.selectbox('Population distribution:',
                         options=distr_list)
    ns = st.select_slider('Sample size:',
                    options=2**np.arange(13), value=32)

    st.markdown(distr)
    if distr == distr_list[0]:
        xs = rd.rand(1000, ns)
        mu, std = 0.5, 1/3**0.5/2
    elif distr == distr_list[1]:
        xs = rd.exponential(1, size=(1000, ns))
        mu, std = 1, 1
    elif distr == distr_list[2]:
        xs = rd.normal(size=(1000, ns))
        mu, std = 0, 1
    elif distr == distr_list[3]:
        xs = rd.randint(low=1, high=7, size=(1000, ns))
        mu, std = 3.5, np.arange(1, 7).std()
    elif distr == distr_list[4]:
        xs = rd.binomial(1, 0.5, size=(1000, ns))
        mu, std = 0.5, 0.5

    xbar = xs.mean(axis=1)

    bins = 20
    xss = xs[0].copy()
    xss.sort()
    fig, ax = plt.subplots(1, 2, figsize=(9, 4.5))
    ax[0].hist(xs[0], bins, color='blue', alpha=0.5)
    ax[0].set_title('Histogram of a sample', fontsize=12)
    ax[0].set_xlabel('Sample data values', fontsize=12)
    ax[0].set_ylabel('Frequency', fontsize=12)
    #xmin, xmax = (xss[0]-mu)/std, (xss[-1]-mu)/std
    #ax[1].plot([xmin, xmax], [xmin, xmax], color='r', linewidth=2)
    ax[1].plot([-3, 3], [-3, 3], color='r', linewidth=2)
    ax[1].scatter(norm.ppf((np.arange(ns)+0.5) / ns),
                  (xss - mu)/std, color='b', alpha=0.3)
    ax[1].set_xlabel('Standard normal quantiles', fontsize=12)
    ax[1].set_ylabel('Ordered standardized values', fontsize=12)
    ax[1].set_title('Q-Q plot of the sample data', fontsize=12)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    xbar.sort()
    fig, ax = plt.subplots(1, 2, figsize=(9, 4.5))
    ax[0].hist(xbar, bins, color='blue', alpha=0.5)
    ax[0].set_title('Histogram of 1000 sample means', fontsize=12)
    ax[0].set_xlabel('Sample means', fontsize=12)
    ax[0].set_ylabel('Frequency', fontsize=12)
    ax[1].plot([-3, 3], [-3, 3], color='r', linewidth=2)
    ax[1].scatter(norm.ppf((np.arange(1000)+0.5) / 1000),
                 (xbar - mu)/std*(ns**0.5), color='b', alpha=0.3)
    ax[1].set_xlabel('Standard normal quantiles', fontsize=12)
    ax[1].set_ylabel('Ordered standardized values', fontsize=12)
    ax[1].set_title('Q-Q plot of 1000 sample means', fontsize=12)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    tx = '- Population mean $\mu$' + ': ${0:0.3f}$ \n '.format(mu)
    tx += '- Population standard deviation $\sigma$' + ': ${0:0.3f}$ \n'.format(std)
    tx += '- Expected value of the sample mean $\\bar{x}$: \n'
    tx += '    - Theoretical value: $\\mathbb{E}(\\bar{x})=\mu=' + '{0:0.3f}'.format(mu) + '$ \n'
    tx += '    - Average of the 1000 sample means: ${0:0.3f}$ \n'.format(xbar.mean())
    tx += '- Standard error of the sample mean $\\bar{x}$: \n'
    tx += '    - Theoretical value: $\\text{SE}(\\bar{x})=\\frac{\\sigma}{\\sqrt{n}}=' + '{0:0.3f}'.format(std/ns**0.5) + '$\n'
    tx += '    - Standard deviation of the 1000 sample means: ${0:0.3f}$ \n'.format(xbar.std())
    st.info(tx)


def conf_int():

    st.markdown('---')
    st.header("Standard Normal Distribution and the $t$-Distribution")
    st.markdown("""Here we compare $t$-distributions with different degree of freedom to the standard
    normal distribution.""")

    norm_t()
    st.markdown("Our observations from the figure above are:")
    st.markdown("""- All $t$-distribution PDF curves are symmetric, bell-shaped, and centered at zero,
    which are similar to the standard normal curve.""")
    st.markdown("""- The difference from the standard normal distribution is that the $t$-distribution
    PDF have more spread than the standard normal distribution. This is because substituting the estimate
    $s$ (which is uncertain) for the fixed parameter $\sigma$ introduces more variation.""")
    st.markdown("""- As the degrees of freedom  $n-1$ increases, the $t$-distribution PDF curve approaches
    the standard normal curve because $s$ estimates $\sigma$ more precisely as the sample size $n$ becomes
    larger. The $t$-distribution PDF would be nearly the same as the standard normal curve under very large
    sample size $n$.
    """)

    st.markdown('---')
    st.header('Confidence Intervals')
    st.markdown("""**Confidence interval** provides a range of plausible values for the unknown population parameter
    (such as the mean). The probability, or confidence that the parameter lies in the confidence interval (i.e.,
    that the confidence interval contains the parameter), is called the **confidence level**, denoted by  $1-\\alpha$
    in this lecture. If $1-\\alpha=95\%$, for instance, we are $95\%$ confident that the true population parameter
    lies within the confidence interval.
    """)

    st.markdown("""In the following example, we repeat a sampling experiment 100 times, and in each experiment, a sample
    with size $n$ is randomly selected from a population following a uniform distribution. The confidence interval for
    estimating the population mean is calculated using the sample data and compared with the true population parameter.
    """)
    ns = st.slider('Sample size: ', min_value=5, max_value=500, step=5)
    alpha = 1 - st.slider('Confidence level: ', min_value=0.85,
                          max_value=0.99, value=0.95, step=0.01)
    cond = st.selectbox('Information on the population standard deviation: ', key='pop sd1',
                        options=['Known standard deviation',
                                 'Unknown standard deviation'])
    t_distr = (cond == 'Unknown standard deviation')
    ci_vis(alpha, ns, 100, t_distr)
    st.markdown("""The definition of the confidence interval suggests that it covers the true value of the population
    mean with a probability of $1-\\alpha$. As a result, in the graph above, if $\\alpha=5\%$, there are roughly (not always)
    $95\%$ of intervals (black lines) capture the true population mean, while the remaining $5\%$ (red lines) cases the
    population mean may fall out of the interval.
    """)

    st.markdown('### Estimating a Population Mean')
    cond = st.selectbox(label="Information on the population standard deviation: ", key='pop sd2',
                        options=['Known standard deviation',
                                 'Unknown standard deviation'])
    t_score = (cond == 'Unknown standard deviation')
    if not t_score:
        st.error(r"""
        $$
        \bar{x} \pm z_{\alpha/2}\cdot\frac{\sigma}{\sqrt{n}}
        $$
        """ +
        r"""- Sample mean: $\bar{x}=\frac{1}{n}\sum_{i=1}^nx_i$
        """ +
        r"""- Cut-off value $z_{\alpha/2}$ as the $(1-\alpha/2)$th percentile of the standard normal distribution
        """ +
        r"""- Known population standard deviation $\sigma$
        """ +
        r"""- Sample size $n$""")
    else:
        st.error(r"""
        $$
        \bar{x} \pm t_{\alpha/2}\cdot\frac{s}{\sqrt{n}}
        $$
        """ +
        r"""- Sample mean: $\bar{x}=\frac{1}{n}\sum_{i=1}^nx_i$
        """ +
        r"""- Cut-off value $t_{\alpha/2}$ as the $(1-\alpha/2)$th percentile of the $t$-distribution with the degree of freedom to be $n-1$
        """ +
        r"""- Sample standard deviation $s$
        """ +
        r"""- Sample size $n$""")

    st.markdown('### Estimating a Population Proportion')
    st.error(r"""
    $$
    \hat{p} \pm z_{\alpha/2}\cdot\sqrt{\frac{\hat{p}(1-\hat{p})}{n}}
    $$
    """ +
    r"""- Sample proportion $\hat{p}$
    """ +
    r"""- Cut-off value $z_{\alpha/2}$ as the $(1-\alpha/2)$th percentile of the standard normal distribution
    """ +
    r"""- Sample size $n$""")

    st.success("""**Example**: Political polling is usually used to predict the results of an election. In
    this example, we focus on how 1) the confidence level $1-\\alpha$; 2) the sample size $n$; and 3) the
    support rate $p$ of a candidate in the overall population, affect the credibility of a poll in terms
    of the margin of error.
    """)

    poll_vis()

    st.markdown('---')
    st.header('Hypothesis Testing')

    htest()


def ci_vis(alpha, n, repeats, t_distr=True):

    mu, std = 0.5, 1/2/3**0.5
    # alpha = 0.05
    fig = plt.figure(figsize=(10, 4.5))

    for i in range(repeats):
        sample = rd.rand(n)
        estimate = sample.mean()
        if t_distr:
            t_alpha2 = t.ppf(1-alpha/2, n-1)
            moe =  t_alpha2 * sample.std() / n**0.5
        else:
            z_alpha2 = norm.ppf(1-alpha/2)
            moe = z_alpha2 * std / n**0.5

        color = 'k' if (estimate + moe > mu and
                        estimate - moe < mu) else 'r'

        plt.errorbar(i, estimate, yerr=moe,
                     c=color, capsize=3,
                     marker='.', markersize=9)

    plt.axhline(mu, c='b')
    plt.xlabel('Experiments', fontsize=12)
    plt.xlim(-3, repeats+2)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)


def norm_t():

    dof = st.slider(label="Degree of freedom:",
                    min_value=1, max_value=15, value=2)

    x_data = np.arange(-4, 4.01, 0.01)

    pdf_normal = norm.pdf(x_data)
    pdf_t_1 = t.pdf(x_data, 1)
    pdf_t_2 = t.pdf(x_data, 2)
    pdf_t_6 = t.pdf(x_data, 6)

    fig = plt.figure(figsize=(6, 5))
    plt.plot(x_data, pdf_normal, linewidth=2, alpha=0.8,
             label='Stanard normal distribution')
    plt.plot(x_data, pdf_t_1, linewidth=2, alpha=0.7, linestyle='--',
             label='t-distribution with d.f.=1')
    plt.plot(x_data, pdf_t_2, linewidth=2, alpha=0.7, linestyle='--',
             label='t-distribution with d.f.=2')
    plt.plot(x_data, pdf_t_6, linewidth=2, alpha=0.7, linestyle='--',
             label='t-distribution with d.f.=6')
    plt.plot(x_data, t.pdf(x_data, dof), color='k', alpha=0.6, linewidth=2.5,
             label='t-distribution with d.f.={}'.format(dof))

    plt.axis(ymax=0.68)

    plt.xlabel('$t$ or $z$ values', fontsize=12)
    plt.ylabel('Probability density function', fontsize=12)
    plt.legend(loc='upper left', fontsize=12)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)


def poll_vis():

    alpha = 1 - st.slider('Confidence level: ', min_value=0.85,
                          max_value=0.99, value=0.95, step=0.01, key='new')
    n = st.slider('Sample size: ', min_value=50, max_value=2500,
                  step=50, value=1000)
    pp = st.slider('Population support rate of a candidate: ',
                   min_value=0.1, max_value=0.9, value=0.3, step=0.05)

    fig = plt.figure(figsize=(7, 4.5))

    ns = np.arange(50, 2550, 50)
    z_alpha2 = norm.ppf(1-alpha/2)
    plt.plot(ns, (z_alpha2 * 0.5/ns**0.5) * 100, linestyle='--',
             linewidth=2, color='b', alpha=0.5,
             label='Maximum Margin of error with $p=0.5$')
    plt.plot(ns, (z_alpha2 * (pp*(1-pp)/ns)**0.5) * 100,
             linewidth=2, color='k', alpha=0.6,
             label='Margin of error with $p=$' + str(pp))
    yn = (z_alpha2 * (pp*(1-pp)/n)**0.5) * 100
    plt.scatter(n, yn, s=60, color='r', alpha=0.5)
    plt.plot([n, n], [0, yn], color='r', linewidth=2, linestyle='--', alpha=0.5)
    plt.plot([-100, n], np.ones(2) * yn, color='r', linewidth=2, linestyle='--', alpha=0.5)
    plt.xlabel('Sample size $n$', fontsize=12)
    plt.ylabel('Margin of error (in percentage)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid()
    plt.yticks(np.arange(0, 20, 2))
    plt.xlim([-100, 2600])
    plt.ylim([0, 17])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)


def htest():

    st.markdown("### Hypotheses")
    options = [r'Population mean when the population standard deviation is known',
               r'Population mean when the population standard deviation is unknown',
               'Population proportion']
    option = st.selectbox(label='Hypothesis test for: ', options=options)

    test_types = ['Left-tailed', 'Right-tailed', 'Two-tailed']
    test = st.selectbox(label='Test type: ', options=test_types)

    if test == test_types[0]:
        op0, op1 = '\geq', '<'
    elif test == test_types[1]:
        op0, op1 = '\leq', '>'
    elif test == test_types[2]:
        op0, op1 = '=', '\\not='

    if option in options[0]:
        distr_label = 'PDF of the standard normal distribution'
        x_label = '$z$ value'
        hypothesis = r"""
        $$
        \begin{cases}
        H_0:~\mu """ + op0 + r""" \mu_0 \\
        H_a:~\mu """ + op1 + r""" \mu_0 \\
        \end{cases}
        $$
        """
        hvalue = r"- Population mean $\mu_0$ assumed in the null hypothesis for testing"
        statistic = r"""
        $$
        z_0 = \frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}
        $$
        """
        distr = r"""follows the standard normal distribution.
        """
        values = (r"""- Sample mean $\bar{x}=\frac{1}{n}\sum_{i=1}^nx_i$
        - Known population standard deviation $\sigma$
        - Sample size $n$""")
    elif option == options[1]:
        distr_label = 'PDF of the $t$-distribution with $n-1$ degree of freedom'
        x_label = '$t$ value'
        hypothesis = r"""
        $$
        \begin{cases}
        H_0:~\mu """ + op0 + r""" \mu_0 \\
        H_a:~\mu """ + op1 + r""" \mu_0 \\
        \end{cases}
        $$
        """
        hvalue = r"- Population mean $\mu_0$ assumed in the null hypothesis for testing"
        statistic = r"""
        $$
        t_0 = \frac{\bar{x}-\mu_0}{s/\sqrt{n}}
        $$
        """
        distr = r"""follows the $t$-distribution with $n-1$ degree of freedom.
        """
        values = (r"""- Sample mean $\bar{x}=\frac{1}{n}\sum_{i=1}^nx_i$
        - Sample standard deviation $s$
        - Sample size $n$""")
    elif option == options[2]:
        distr_label = 'PDF of the standard normal distribution'
        x_label = '$z$ value'
        hypothesis = r"""
        $$
        \begin{cases}
        H_0:~p """ + op0 + r""" p_0 \\
        H_a:~p """ + op1 + r""" p_0 \\
        \end{cases}
        $$
        """
        hvalue = r"- Population proportion $p_0$ assumed in the null hypothesis for testing"
        statistic = r"""
        $$
        z_0 = \frac{\hat{p}-p_0}{\sqrt{p_0(1-p_0)/n}}
        $$
        """
        distr = r"""follows the standard normal distribution.
        """
        values = (r"""- Sample proportion $\hat{p}$
        - Sample size $n$
                  """)

    st.error(hypothesis + hvalue)

    st.markdown('### The test stastistics')
    st.error(statistic + distr + values)

    st.markdown('### Calculate the $P$-value')
    stat_value = st.slider(label='Value of the test statistics: ',
                           min_value=-4.0, max_value=4.0, value=-1.5, step=0.1)
    ns = st.slider(label='Sample size: ',
                   min_value=5, max_value=200, value=25, step=5)
    if option == options[0]:
        stat_distr = norm(0, 1)
        stat_var = 'z_0'
    elif option == options[1]:
        stat_distr = t(df=ns-1)
        stat_var = 't_0'
    elif option == options[2]:
        stat_distr = norm(0, 1)
        stat_var = 'z_0'

    x_data = np.arange(-4, 4.01, 0.01)
    fig = plt.figure(figsize=(7, 4))
    if test == test_types[0]:
        y_pdf = stat_distr.pdf(x_data)
        plt.plot(x_data, y_pdf, linewidth=2, color='k', alpha=0.5, label=distr_label)
        xf = np.arange(-4, stat_value+0.01, 0.01)
        p_value = stat_distr.cdf(stat_value)
        plt.fill_between(xf, y1=0, y2=stat_distr.pdf(xf),
                         color='b', alpha=0.6,
                         label='$P$-value: {0:0.4f}'.format(p_value))
        plt.scatter(stat_value, stat_distr.pdf(stat_value),
                    s=60, color='r', alpha=0.5)
        plt.plot(np.ones(2) * stat_value, [0, stat_distr.pdf(stat_value)],
                 color='r', alpha=0.6, linewidth=2, linestyle='--',
                 label='Value of the test statistic ${}$'.format(stat_var))
    elif test == test_types[1]:
        y_pdf = stat_distr.pdf(x_data)
        plt.plot(x_data, y_pdf, linewidth=2, color='k', alpha=0.5, label=distr_label)
        xf = np.arange(stat_value+0.01, 4.01, 0.01)
        p_value = 1 - stat_distr.cdf(stat_value)
        plt.fill_between(xf, y1=0, y2=stat_distr.pdf(xf),
                         color='b', alpha=0.6,
                         label='$P$-value: {0:0.4f}'.format(p_value))
        plt.scatter(stat_value, stat_distr.pdf(stat_value),
                    s=60, color='r', alpha=0.5)
        plt.plot(np.ones(2) * stat_value, [0, stat_distr.pdf(stat_value)],
                 color='r', alpha=0.6, linewidth=2, linestyle='--',
                 label='Value of the test statistic ${}$'.format(stat_var))
    elif test == test_types[2]:
        y_pdf = stat_distr.pdf(x_data)
        plt.plot(x_data, y_pdf, linewidth=2, color='k', alpha=0.5, label=distr_label)
        xf = np.arange(-4, -abs(stat_value)+0.01, 0.01)
        p_value = 2 * stat_distr.cdf(-abs(stat_value))
        plt.fill_between(xf, y1=0, y2=stat_distr.pdf(xf),
                         color='b', alpha=0.6)
        xf = np.arange(abs(stat_value), 4.01, 0.01)
        plt.fill_between(xf, y1=0, y2=stat_distr.pdf(xf),
                         color='b', alpha=0.6,
                         label='$P$-value: {0:0.4f}'.format(p_value))
        plt.scatter(stat_value, stat_distr.pdf(stat_value),
                    s=60, color='r', alpha=0.5)
        plt.plot(np.ones(2) * stat_value, [0, stat_distr.pdf(stat_value)],
                 color='r', alpha=0.6, linewidth=2, linestyle='--',
                 label='Value of the test statistic ${}$'.format(stat_var))
    plt.ylabel('Probability density function', fontsize=12)
    plt.xlabel(x_label, fontsize=12)
    plt.legend(loc='upper left', fontsize=11)
    plt.ylim([-0.04, 0.64])

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.markdown("### Conclusion")
    st.error("""Given a significant level $\\alpha$, we draw conclusions from the $P$-value: \n- We reject
    the null hypothesis $H_0$ in favor of the alternative hypothesis, if the $P$-value is **lower** than the
    selected significance level $\\alpha$;\n- Otherwise, we do not reject the null hypothesis.
    """)


def pred_regress():

    st.markdown('---')
    st.header('Regression for Predictive Modeling')
    st.markdown("""Suppose that a quantitative response $y$ and $p$ different predictors,
    $\pmb{x}=\left(x_1, x_2, ..., x_p\\right)$ are observed. The relationship between $y$
    and $\pmb{x}$ is assumed to follow the general form
    """)
    st.markdown(r"""
    $$
    y = f(\pmb{x}) + u,
    $$
    """)
    st.markdown("""where $f$ is some fixed but unknown function of predictors $\pmb{x}$ and
    $u$ is a random error term that is independent of $\pmb{x}$ and has mean zero. In the
    context of predictive modeling, we are interested in predicting $y$ using
    """)
    st.markdown(r"""
    $$
    \hat{y} = \hat{f}(\pmb{x}),
    $$""")
    st.markdown("""where $\hat{y}$ is the predicted value of $y$, and $\hat{f}$ represents our
    estimate for the unknown function $f$, which is typically obtained using a training dataset
    $\left\{(\pmb{x}_1, y_1), (\pmb{x}_2, y_2), \dots, (\pmb{x}_n, y_n)\\right\}$. In the
    regression setting, a commonly-used approach for identifying $\hat{f}$ is to minimize the
    **mean squared error (MSE)**, given by
    """)
    st.markdown(r"""
    $$
    \text{MSE} = \frac{1}{n}\sum\limits_{i=1}^n\left(y_i - \hat{f}(\pmb{x}_i)\right)^2.
    $$
    """)
    st.markdown("""The MSE term computed above using the training dataset is refer to as the
    **training MSE**. In assessing the performance of the model, we are more interested in the
    prediction accuracy as $\hat{f}$ is applied to previously unseen test observations rather
    than the training dataset, so models with the lowest **test MSE** is preferred.
    """)
    st.markdown("""Let $(\pmb{x}_0, y_0)$ be a test observation, the expected test MSE can be written as
    """)
    st.markdown(r"""
    $$
    \begin{array}{rl}
    \mathbb{E}\left(y_0 - \hat{f}(\pmb{x}_0)\right)^2
    =& \mathbb{E}\left(f(\pmb{x}_0) + u - \hat{f}(\pmb{x}_0)\right)^2 \\
    =& \mathbb{E}\left(f(\pmb{x}_0) - \hat{f}(\pmb{x}_0)\right)^2 + \text{Var}(u) \\
    =& \mathbb{E}\left(f(\pmb{x}_0) - \mathbb{E}\left(\hat{f}(\pmb{x}_0)\right) +
    \mathbb{E}\left(\hat{f}(\pmb{x}_0)\right) - \hat{f}(\pmb{x}_0)\right)^2 + \text{Var}(u) \\
    =& \left(f(\pmb{x}_0) - \mathbb{E}\left(\hat{f}(\pmb{x}_0)\right)\right)^2 +
    \text{Var}\left(\hat{f}(\pmb{x}_0)\right) + \text{Var}(u),
    \end{array}
    $$
    """)
    st.markdown(""" where

    - The first term represents the expected squared **bias** of $\hat{f}(\pmb{x}_0)$;
    - The second term measures the **variance** of $\hat{f}(\pmb{x}_0)$;
    - The last term is the variance of the random error $u$, which is independent from the
    model and cannot be reduced, thus called **irreducible error**.
    """)

    st.markdown("""It can be seen that in predictive modeling, the minimum test MSE is achieved as the
    combination of bias and variance is minimized.
    """)

    st.success("""**Example**: A training dataset with 30 observations is generated from a mysterious function $f$,
    and we use a polynomial regression model with $k$ polynomial terms to predict the value of response $y$. Use the
    experiments below to explore the trade-off between the bias and variance of the estimate $\hat{f}$ and how the
    paramter $k$ affects the training and test MSEs.
    """)

    train = rand_xy(30)
    test = rand_xy(20)

    k = st.slider(label='The number of polynomial terms: ',
                  min_value=1, max_value=25, value=5, step=1)
    options = ['Training set', 'Fitted values', 'Test set']
    show = st.multiselect(label='Display options: ',
                          options=options, default=options[:2])
    srf = polyfit(train, k)

    # fig = plt.figure(figsize=(5.7, 4.3))
    fig, ax = plt.subplots(2, 1, figsize=(5.7, 7))
    if options[0] in show:
        ax[0].scatter(train['x'], train['y'], color='b', alpha=0.3, s=30,
                      label=options[0])
    if options[2] in show:
        ax[0].scatter(test['x'], test['y'], color='r', alpha=0.3, s=30,
                      label=options[2])

    if options[1] in show:
        xx = np.arange(0, 1.01, 0.01)
        ax[0].plot(xx, srf.predict({'x': xx}), color='m', linewidth=2, alpha=0.4,
                   label=options[1])
    ax[0].legend(loc='upper left', fontsize=11)
    # ax[0].set_xlabel('Variable $x$', fontsize=12)
    ax[0].set_ylabel('Predicted variable $y$', fontsize=12)
    ax[0].set_xlim([-0.05, 1.05])
    ax[0].set_ylim([-2, 27])
    ax[0].set_title('Bias-variance trade-off', fontsize=12)

    repeat = 30
    # fig = plt.figure(figsize=(5.7, 4.3))
    XX = np.arange(0, 1.01, 0.01).reshape((101, 1)) ** np.arange(1, 26)
    for b in range(repeat):
        x, y = dyn_xy(50)
        X = x.reshape((x.size, 1)) ** np.arange(1, 26)
        x_train, x_test, y_train, y_test = train_test_split(X[:, :k], y,
                                                            test_size=0.4, shuffle=True)
        regr = LinearRegression()
        regr.fit(x_train, y_train)
        xx = np.arange(0, 1.01, 0.01)
        yy = regr.predict(XX[:, :k])
        if b == 0:
            ax[1].plot(xx, yy, color='m', alpha=0.3, label='Fitted values')
        else:
            ax[1].plot(xx, yy, alpha=0.3, color='m')
    yy = ((1.2 - 0.2*xx) * np.sin(11*xx) + 4*xx) * 4
    ax[1].plot(xx, yy, color='g', linewidth=2.5, label='True population function')
    ax[1].legend(fontsize=11)
    ax[1].set_xlabel('Predictor variable $x$', fontsize=12)
    ax[1].set_ylabel('Predicted variable $y$', fontsize=12)
    ax[1].set_xlim([-0.05, 1.05])
    ax[1].set_ylim([-2, 27])
    # ax[1].set_title('Model fitted to 30 random training datasets', fontsize=12)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.markdown("""The experiments above show that a relative simpler model, such as a model that hass
    only a linear term or a small number of polynomial terms, it is less flexible and may not closely
    follow the trend of the observed training data points, thus leading to larger bias of the fitted
    model. As the parameter $k$ increases, the model is more flexible and the bias of $\hat{f}$ is greatly
    reduced as it better follows the observed training data points, but it is at the expense of rapidly
    increasing variance of $\hat{f}$. As shown by the plot at the bottom, the fitted curves exhibit wild
    oscillations, in cases of very large $k$ values. In this regression model, such large oscillations can
    be partially explained by the huge model parameters, as shown by the figure below.
    """)

    repeat = 100
    all_mse_train = []
    all_mse_test = []
    all_coef_mag = []
    XX = np.arange(0, 1.01, 0.01).reshape((101, 1)) ** np.arange(1, 26)
    for k in range(1, 13):
        mse_train = 0
        mse_test = 0
        coef_mag = 0
        for b in range(repeat):
            x, y = dyn_xy(50)
            X = x.reshape((x.size, 1)) ** np.arange(1, 26)
            x_train, x_test, y_train, y_test = train_test_split(X[:, :k+1], y,
                                                                test_size=0.4)
            regr = LinearRegression()
            regr.fit(x_train, y_train)
            mse_train += ((regr.predict(x_train) - y_train) ** 2).mean() /repeat
            mse_test += ((regr.predict(x_test) - y_test) ** 2).mean() /repeat
            coef_mag += (abs(regr.coef_).mean()) / repeat

        all_mse_train.append(mse_train)
        all_mse_test.append(mse_test)
        all_coef_mag.append(coef_mag)

    # fig = plt.figure(figsize=(5.7, 4.3))
    fig, ax = plt.subplots(2, 1, figsize=(5.7, 7))

    ax[1].plot(range(1, 13), all_mse_train,
             linewidth=2, color='b', marker='s', label='Training MSE')
    ax[1].plot(range(1, 13), all_mse_test,
             linewidth=2, color='r', marker='s', label='Test MSE')
    ax[1].legend(loc='upper left', fontsize=11)
    ax[1].set_xlabel('Number of predictor variables', fontsize=12)
    ax[1].set_ylabel('Average MSE', fontsize=12)
    ax[1].set_ylim([0.1, 1e7])
    ax[1].set_xlim([0.5, 12.5])
    ax[1].set_yscale('log')
    ax[1].set_xticks(range(1, 13))

    ax[0].set_title('Experiments on 100 random training/test datasets', fontsize=12)
    ax[0].plot(range(1, 13), all_coef_mag,
               linewidth=2, color='b', marker='s', label='Average magnitude of coefficients')
    ax[0].legend(fontsize=12)
    ax[0].set_yscale('log')
    # ax[0].set_xlabel('Number of predictor variables', fontsize=12)
    ax[0].set_ylabel('Magnitudes of coefficients', fontsize=12)
    ax[0].set_xlim([0.5, 12.5])
    ax[0].set_ylim([0.1, 1e10])
    ax[0].set_xticks(range(1, 13))

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.markdown("""The bottom plot above shows the U-shaped trend of the test MSE as we increase the
    level of flexibility of a model. When the $k$ value is too small, the model is considered to be
    **underfitting** as both the training and test MSEs are high as a result of the high bias. As the
    model becomes too flexible, though the trianing MSE is small, the test MSE may be extremely large
    due to the high variance, and such a behavior is known as **overfitting**. The test MSE is minimized
    when the model simultaneously achieves low bias and low variance.
    """)

def reduce_dim():

    st.markdown("---")
    st.header("Dimension Reduction")

    curse_dim()


def curse_dim():

    st.markdown("### Curse of Dimensionality")
    st.success("""**Example**: In the following simulaiton, a training dataset with 10,000
    observations are random generated assuming that each variable is independent and follows
    a uniform distribution between zero and one. The histograms below show the influence of
    data dimensions on the distance from these data points to borders and test data records.
    """)

    dim = st.slider(label='Dimension of the training dataset',
                    min_value=1, max_value=50, value=5, step=1)

    train_obs = rd.rand(10000, dim)
    dist_border = np.minimum(train_obs.min(axis=1), (1-train_obs).min(axis=1))

    fig, ax = plt.subplots(2, 1, figsize=(5.7, 7))
    ax[0].hist(dist_border, bins=np.arange(0, 0.51, 0.01), color='b', alpha=0.4)
    ax[0].set_xlabel('Minimum distance to the border', fontsize=12)
    ax[0].set_ylabel('Frequency', fontsize=12)

    test_obs = rd.rand(1, dim)
    dist_test = ((train_obs - test_obs)**2).sum(axis=1) ** 0.5
    ax[1].hist(dist_test, bins=np.arange(0, 5.05, 0.05), color='b', alpha=0.4)
    ax[1].set_xlabel('Distance to the a test data point', fontsize=12)
    ax[1].set_ylabel('Frequency', fontsize=12)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.markdown('''The experiments above show that as the dimension increases, the training data points
    tend to be "extreme" as they approach at least one of the borders, and the distance betwen the test
    observation is farther away from the training dataset, so it is more difficult to make an accurate
    predictio for the test data.
    ''')

def pca_vis():

    data = pd.read_csv('USArrests.csv')

    st.markdown('### Pricipal Component Analysis')
    st.success("""**Example**: The [`USArrests`](https://github.com/XiongPengNUS/learn_dao/blob/main/USArrests.csv)
    dataset below provides the crime statistics per 100,000 residents in 50 states of USA. Here we use two variables
    of the dataset to illustrate how principal component analysis is applied to reduce data dimensions.
    """)
    # st.write(data)
    st.dataframe(data, height=180)

    columns = data.columns[1:]
    col1, col2 = st.columns(2)

    with col1:
        xvar = st.radio(label='Variable as X-data', options=columns, index=0)
    with col2:
        yvar = st.radio(label='Variable as Y-data', options=columns, index=1)

    xs = (data[xvar] - data[xvar].mean()) / data[xvar].std()
    ys = (data[yvar] - data[yvar].mean()) / data[yvar].std()
    ds = np.array([xs, ys]).T
    pca = PCA(n_components=1).fit(ds)
    theta = pca.components_
    z0 = ds[:, 0]*theta[0, 0] + ds[:, 1]*theta[0, 1]
    z1 = - ds[:, 0]*theta[0, 1] + ds[:, 1]*theta[0, 0]

    fig, ax = plt.subplots(2, 2, figsize=(7.5, 7.5))

    ax[0, 0].scatter(data[xvar], data[yvar], alpha=0.4, color='b')
    ax[0, 0].set_xlabel(xvar, fontsize=12)
    ax[0, 0].set_ylabel(yvar, fontsize=12)
    ax[0, 0].set_title('Subplot (a)', fontsize=14)

    ax[0, 1].scatter(xs, ys, alpha=0.4, color='b')
    ax[0, 1].set_xlabel('Standardized value of ' + xvar, fontsize=12)
    ax[0, 1].set_ylabel('Standardized value of ' + yvar, fontsize=12)

    slope = theta[0, 0] / theta[0, 1]
    intercept = 0
    x0 = np.arange(-2.5, 2.6, 0.1)
    # ax[1, 0].scatter(xs, ys, alpha=0.4, color='b')
    ax[0, 1].plot(x0, intercept + slope*x0, linewidth=2.5, color='r')

    x0p = (ds[:, 0] + (ds[:, 1] - intercept)*slope) / (slope**2 + 1)
    x1p = slope * x0p + intercept
    for i in range(ds.shape[0]):
        ax[0, 1].plot([ds[i, 0], x0p[i]], [ds[i, 1], x1p[i]],
                      color='m', linewidth=1, linestyle='--')
    ax[0, 1].axis('equal')
    ax[0, 1].set_title('Subplot (b)', fontsize=14)


    ax[1, 0].scatter(z0, z1, c='b', alpha=0.3)
    ax[1, 0].hlines(y=0, xmin=-3, xmax=3, linewidth=2, color='r')
    for i in range(ds.shape[0]):
        ax[1, 0].plot([z0[i], z0[i]], [0, z1[i]],
                      color='m', linewidth=1, linestyle='--')

    ax[1, 0].set_xlabel('The 1st principal component', fontsize=12)
    ax[1, 0].set_ylabel('The 2nd principal component', fontsize=12)
    ax[1, 0].axis('equal')
    ax[1, 0].set_title('Subplot (c)', fontsize=14)

    ax[1, 1].scatter(z0, np.zeros(z1.shape), c='b', alpha=0.3)
    ax[1, 1].hlines(y=0, xmin=-3, xmax=3, linewidth=2, color='r')
    ax[1, 1].set_xlabel('The 1st principal component', fontsize=12)
    ax[1, 1].set_ylabel('The 2nd principal component', fontsize=12)
    ax[1, 1].axis('equal')
    ax[1, 1].set_title('Subplot (d)', fontsize=14)

    fig.tight_layout(pad=1.5)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    st.image(buf)

    st.markdown("In the figure above:\n" +
    f"""- Subplot (a) shows the data of two selected variables `{xvar}` and `{yvar}`. The correlation
    between these two variables is {data.corr().loc[xvar, yvar]:0.4f}.\n""" +
    """- Subplot (b) shows the standardized values of the selected variables, and displays two
    perpendicular components that captures the variation of these two variables.\n""" +
    """- Subplot (c) shows that the first principal component captures most of the variation of these
    two variables, and the remaining variation is represented by the second principal component.\n""" +
    """- Subplot (d) shows that as the second principal component is removed, the dimension of data is
    reduced while the first component preserves most of (not all) the variation information in the
    selected variable.""")



def polyfit(data, k):

    formula = 'y ~ ' + ' + '.join(['np.power(x, {})'.format(i)
                                   for i in range(1, k+1)])
    return smf.ols(formula, data).fit()


#@st.cache
def dyn_xy(n):

    x = rd.rand(n)
    y = ((1.2 - 0.2*x) * np.sin(11*x) + 4*x) * 4 + rd.randn(n)

    return x, y


@st.cache
def rand_xy(n):

    x = rd.rand(n)
    y = ((1.2 - 0.2*x) * np.sin(11*x) + 4*x) * 4 + rd.randn(n)

    return pd.DataFrame({'y': y, 'x': x})


def exp_regress():

    st.markdown('---')
    st.header('Notations')

    st.markdown("A linear regression model can be generalized as the equation")
    st.markdown(r"""
    $$
    y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + ... + \beta_p x_p + u,
    $$""")
    st.markdown("""where $\\beta_0, \\beta_1, ..., \\beta_p$ are parameters of the model.
    Notations of the regression model are summarized in the table below.
    """)

    st.markdown("""
    Notation Types | Notations
    :-------------|:--------------
    Variables | $x_j$, $y$, $u$
    Data samples (the $i$th) | $x_{ij}$, $y_i$
    Sample averages | $\\bar{x}_j$, $\\bar{y}$
    Estimates from data (Estimates) | $\\hat{y}$, $\\hat{u}_i$, $\\hat{\\beta}_0$, $\\hat{\\beta}_j$
    """)

    st.markdown('\n')
    st.markdown("""and we use a simple regression model $y=\\beta_0 + \\beta_1x_1 + u$ to
    illustrate the correponding notations.
    """)

    options = ['Sample regression function (SRF)',
               'Population regression function (PRF)',
               'Residuals']
    show = st.multiselect(label='Notations',
                          options=options,
                          default=['Sample regression function (SRF)'])

    refresh = st.button(label='Generate New Dataset')
    if refresh:
        # caching.clear_cache()
        # st.experimental_memo.clear()
        st.caching.memo.clear()

    data = xydata(1, 5, 20)

    fig = plt.figure(figsize=(5.5, 4.2))
    xi, yi = data['x'], data['y']
    plt.scatter(xi, yi, c='b', alpha=0.3, s=40,
                label='The sample data              ')

    result = smf.ols('y ~ x', data).fit()

    if options[0] in show:
        xs = np.arange(2)
        ys = result.predict({'x': xs})
        plt.plot(xs, ys, c='r', linewidth=3, alpha=0.5,
                 label=r'SRF $\hat{y}=\hat{\beta}_0+\hat{\beta}_1x_1$')
    if options[1] in show:
        xs = np.arange(2)
        ys = 1 + 5*xs
        plt.plot(xs, ys, c='m', linewidth=3, linestyle='--', alpha=0.5,
                 label=r'PRF $\mathbb{E}(y|x_1)=\beta_0 + \beta_1 x_1$')
    if options[2] in show:
        ys = result.predict({'x': xi})
        us = yi - ys
        yerr = np.vstack((np.zeros(20), us))
        plt.errorbar(xi, ys, yerr=yerr,
                     linestyle='None', c='b', alpha=0.5,
                     elinewidth=2, capthick=2, capsize=3,
                     label='Residuals $\hat{u}_i$')

    plt.legend(fontsize=12, bbox_to_anchor=(1.02, 1.03), loc='upper left')
    plt.xlabel('Independent variable $x_1$', fontsize=12)
    plt.ylabel('Dependent variable $y$', fontsize=12)

    plt.ylim([-1.2, 8.2])

    attr = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    message = 'True parameters:    Fitted values: \n'
    message += r'$\beta_0=$' + '{0:.1f}                   '.format(1)
    message += r'$\hat{\beta}_0=$' + '{0:.3f}\n'.format(result.params[0])
    message += r'$\beta_1=$' + '{0:.1f}                   '.format(5)
    message += r'$\hat{\beta}_1=$' + '{0:.3f}'.format(result.params[1])
    plt.text(1.11, -0.75, message, fontsize=13, bbox=attr)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.image(buf)


    st.markdown('---')
    st.header('The Ordinary Least Squares (OLS) Method')
    st.markdown("""The ordinary least squares (OLS) method is a commonly used method
    to estimate coefficients of regression models. Consider the dataset below with
    20 recrods of the dependent variable $y$ and independent variable $x$.
    """)
    # st.write(data)
    st.dataframe(data, height=120)
    st.markdown("""The model can be fitted using the OLS tools provided in the `statsmodels`
    package:\n\n""" +
    '1. Import the module `statsmodels.formula.api`;\n' +
    """2. Define a linear regression model by the `ols()` function. The formula is given as a string,
    where the dependent variable and independent variable are indicated by the corresponding
    column labels of the dataset;\n""" +
    """3. Calcualte the model parameters and statistics by calling the `fit()` method of the model
    object;\n""" +
    """4. Print the results exported by the `summary()` method.""")

    st.markdown("""
    ```python
    import statsmodels.formula.api as smf

    model = smf.ols('y ~ x',    # Formula: dependent variable y, independent variable x
                    data=data)  # Variable 'data' as the dataset
    result = model.fit()        # Calculate the fitted model parameters
    print(result.summary())     # Print the summary of results
    ```
    """)

    st.markdown('Results of running the regression model are summarized as folows.')
    summary = smf.ols('y ~ x', data).fit().summary().__str__()
    st.markdown("```python\n" + summary)

    st.markdown('---')
    st.header('Goodness-of-Fit')

    st.markdown("""The **R-squared value** of the regression, sometimes called the **coefficient
    of determination**, is defined as""")
    st.markdown("""
    $$
    R^2 = \\frac{\\text{SSE}}{\\text{SST}} = 1 = \\frac{\\text{SSR}}{\\text{SSE}}
    $$
    """)
    st.markdown("where\n" +
                """- SST: the **total sum of squares**, which measures the total variations
                in the sample data $y_i$;\n""" +
                """- SSE: the **explained sum of squares**, which measure the variation
                in the fitted value $\\hat{y}_i$\n""" +
                """- SSR: the **residual sum of squared**, which measure the variation in
                residuals $\\hat{u}_i$\n""")
    st.markdown("""The data visual below illustrates each component of variations and we always
    have""")
    st.markdown("""
    $$
    \\text{SST} = \\text{SSE} + \\text{SSR}
    $$""")

    options = ['Total variations',
               'Explained terms',
               'Unexplained terms']
    show = st.radio(label='Components of variations',
                    options=options)

    fig = plt.figure(figsize=(5.5, 4.2))
    xi, yi = data['x'], data['y']
    plt.scatter(xi, yi, c='b', alpha=0.3, s=40,
                label='The sample data              ')
    plt.plot([0, 1], np.ones(2)*yi.mean(), linestyle='--', linewidth=2, c='m',
             label='Sample average $\overline{y}$')
    xs = np.arange(2)
    ys = result.predict({'x': xs})
    plt.plot(xs, ys, c='r', linewidth=3, alpha=0.5,
             label=r'SRF $\hat{y}=\hat{\beta}_0+\hat{\beta}_1x_1$')

    if show == options[0]:
        tv = yi - yi.mean()
        yerr = np.vstack((np.zeros(20), tv))
        plt.errorbar(xi, yi.mean()*np.ones(20), yerr=yerr,
                     c='b', alpha=0.5, elinewidth=2, capthick=2, capsize=3, linewidth=0,
                     label='Total variation: $y_i-\overline{y}$')
    if show == options[1]:
        ys = result.predict({'x': xi})
        ev = ys - yi.mean()
        yerr = np.vstack((np.zeros(20), ev))
        plt.errorbar(xi, yi.mean()*np.ones(20), yerr=yerr,
                     c='r', alpha=0.5, elinewidth=2, capthick=2, capsize=3, linewidth=0,
                     label='Explained term: $\hat{y}_i-\overline{y}$')
    if show == options[2]:
        ys = result.predict({'x': xi})
        uv = yi - ys
        yerr = np.vstack((np.zeros(20), uv))
        plt.errorbar(xi, ys, yerr=yerr,
                     c='g', alpha=0.5, elinewidth=2, capthick=2, capsize=3, linewidth=0,
                     label='Unexplained term: $\hat{y}_i-y_i$')

    plt.legend(fontsize=12, bbox_to_anchor=(1.02, 1.03))
    plt.xlabel('Independent variable $x_1$', fontsize=12)
    plt.ylabel('Dependent variable $y$', fontsize=12)

    plt.ylim([-1.2, 8.2])

    ys = result.predict({'x': xi})
    sst = ((yi - ys.mean()) ** 2).sum()
    sse = ((ys - ys.mean()) ** 2).sum()
    ssr = ((yi - ys) ** 2).sum()

    attr = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    message = r'SST$=\sum_{i=1}^n(y_i - \bar{y})^2=$' + '{0:.4f}    \n'.format(sst)
    message += r'SSE$=\sum_{i=1}^n(\hat{y}_i - \bar{y})^2=$' + '{0:.4f}    \n'.format(sse)
    message += r'SSR$=\sum_{i=1}^n(\hat{y}_i - y_i)^2=$' + '{0:.4f}    '.format(ssr)
    plt.text(1.11, -0.35, message, fontsize=13, bbox=attr)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.image(buf)


def pred_class():

    st.markdown('---')
    st.header('Classification for Prediction Modeling')
    st.markdown("""Here, we create a simulated dataset such that\n- There are
    two independent variables,  $x_1$ and  $x_2$;\n- The response variable $y$
    may belong to one of two classes;\n- For both classes, 30 observations are
    randomly generated.
    """)
    st.markdown("""The dataset are generated following different patterns
    such that these two classes may be 1) separable by a hyperplane; 2) barely
    separable by a hyperplane; or 3) non-separable by a hyperplane.
    """)

    options = ['Separable', 'Barely separable', 'Non-separable']
    option = st.radio(label='Separable by a hyperplane', options=options)

    x, y = two_class_data(30, option)

    st.markdown("""You may use the following models to fit the dataset with
    different patterns.
    """)

    models = ['None',
              'Logistic regression',
              'Linear discriminant analysis',
              'Quadratic discriminant analysis',
              'Support vector machine',
              'K-nearest neighbors']

    pred_model = st.selectbox(label='Classification model', options=models)

    fig = plt.figure(figsize=(4.5, 4.5))
    if pred_model == models[1]:

        expd = st.expander('Model and display options', expanded=False)
        with expd:
            disp_options = ['Prediction', 'Predicted probability of Class 1']
            display = st.multiselect(label='Display options',
                                     options=disp_options)
        cls = LogisticRegression()
        cls.fit(x, (y+1)/2)

        xx, yy = np.meshgrid(np.arange(-3, 5.52, 0.02),
                             np.arange(-3, 5.52, 0.02))
        # xx, yy = xx.reshape((xx.size, 1)), yy.reshape((yy.size, 1))
        xdata = np.hstack((xx.reshape((xx.size, 1)), yy.reshape((yy.size, 1))))
        zz = cls.predict(xdata)
        proba = cls.predict_proba(xdata)[:, 0]

        zz = zz.reshape(xx.shape)
        proba = proba.reshape(xx.shape)

        if not display:
            plt.contour(xx, yy, proba, levels=[0.5],
                        colors=['k'], linestyles=['-'])
        if disp_options[0] in display:
            plt.contourf(xx, yy, zz, 10, alpha=0.2, colors=['r', 'b'])
        if disp_options[1] in display:
            ct = plt.contour(xx, yy, proba, levels=[0.1, 0.3, 0.5, 0.7, 0.9],
                             colors=['k'], linestyles=[':', '--', '-', '--', ':'])
            plt.clabel(ct, [0.1, 0.3, 0.5, 0.7, 0.9], fontsize=10)
    elif pred_model == models[2]:
        expd = st.expander('Model and display options', expanded=False)
        with expd:
            disp_options = ['Prediction', 'PDF contours']
            display = st.multiselect(label='Display options',
                                     options=disp_options)

        cls = LinearDiscriminantAnalysis()
        cls.fit(x, y)

        xx, yy = np.meshgrid(np.arange(-3, 5.52, 0.02),
                             np.arange(-3, 5.52, 0.02))
        xdata = np.hstack((xx.reshape((xx.size, 1)), yy.reshape((yy.size, 1))))
        zz = cls.predict_proba(xdata)[:, 1].reshape(xx.shape)

        plt.contour(xx, yy, zz, levels=[0.5],
                    colors=['k'], linestyles=['-'])

        if disp_options[0] in display:
            zp = np.ones(zz.shape)
            zp[zz < 0.5] = -1

            plt.contourf(xx, yy, zp, 10, alpha=0.2, colors=['r', 'b'])
        if disp_options[1] in display:
            c1 = x[y==1]
            c2 = x[y==-1]
            mu1 = c1.mean(axis=0)
            mu2 = c2.mean(axis=0)
            cov = (np.cov(c2.T) + np.cov(c1.T))/2

            xx, yy = np.meshgrid(np.arange(-3, 5.52, 0.02),
                                 np.arange(-3, 5.52, 0.02))
            z1 = multivariate_normal.pdf(np.array([xx, yy]).transpose((1, 2, 0)), mu1, cov)
            z2 = multivariate_normal.pdf(np.array([xx, yy]).transpose((1, 2, 0)), mu2, cov)
            zf = np.maximum(z1, z2)

            levels = np.percentile(zf.reshape(zf.size), [20, 40, 60, 80, 90, 95, 98])
            ct = plt.contour(xx, yy, zf, levels=levels, linestyles=['--']*7)
    elif pred_model == models[3]:
        expd = st.expander('Model and display options', expanded=False)
        with expd:
            disp_options = ['Prediction', 'PDF contours']
            display = st.multiselect(label='Display options',
                                     options=disp_options)

        cls = QuadraticDiscriminantAnalysis()
        cls.fit(x, y)

        xx, yy = np.meshgrid(np.arange(-3, 5.52, 0.02),
                             np.arange(-3, 5.52, 0.02))
        xdata = np.hstack((xx.reshape((xx.size, 1)), yy.reshape((yy.size, 1))))
        zz = cls.predict_proba(xdata)[:, 1].reshape(xx.shape)

        plt.contour(xx, yy, zz, levels=[0.5],
                    colors=['k'], linestyles=['-'])

        if disp_options[0] in display:
            zp = np.ones(zz.shape)
            zp[zz < 0.5] = -1
            plt.contourf(xx, yy, zp, 10, alpha=0.2, colors=['r', 'b'])
        if disp_options[1] in display:
            c1 = x[y==1]
            c2 = x[y==-1]
            mu1 = c1.mean(axis=0)
            mu2 = c2.mean(axis=0)
            cov1 = np.cov(c1.T)
            cov2 = np.cov(c2.T)

            xx, yy = np.meshgrid(np.arange(-3, 5.52, 0.02),
                                 np.arange(-3, 5.52, 0.02))
            z1 = multivariate_normal.pdf(np.array([xx, yy]).transpose((1, 2, 0)), mu1, cov1)
            z2 = multivariate_normal.pdf(np.array([xx, yy]).transpose((1, 2, 0)), mu2, cov2)
            zf = np.maximum(z1, z2)

            levels = np.percentile(zf.reshape(zf.size), [20, 40, 60, 80, 90, 95, 98])
            ct = plt.contour(xx, yy, zf, levels=levels, linestyles=['--']*7)
    elif pred_model == models[4]:

        expd = st.expander('Model and display options', expanded=False)
        with expd:
            c_value = st.select_slider(label='Regularization parameter',
                                       options=2.0**np.arange(-6, 11), value=1,
                                       format_func=(lambda x: round(x, 2)))
            kernels = ['linear', 'poly', 'rbf', 'sigmoid']
            kernel = st.selectbox(label='Kernel type', options=kernels)
            degree = st.slider(label='Degree of polynomial kernels (ineffective for other types of kernels)',
                               min_value=1, max_value=9, value=3, step=1)
            gamma = st.select_slider(label='Gamma parameter of nonliner kernels (ineffective for linear and polynomial kernels)',
                                     options=2.0**np.arange(-5, 6), value=0.5,
                                     format_func=(lambda x: round(x, 2)))
            coef0 = st.slider(label='Constant coefficient (ineffective for linear and rbf kernels)',
                              min_value=0, max_value=10, value=1, step=1)
            disp_options = ['Prediction', 'Margin', 'Support vectors']
            display = st.multiselect(label='Display options',
                                     options=disp_options)

        cls = SVC(C=c_value, kernel=kernel, degree=degree, gamma=gamma, coef0=coef0, max_iter=1e8)
        cls.fit(x, y)

        xx, yy = np.meshgrid(np.arange(-3, 5.52, 0.02),
                             np.arange(-3, 5.52, 0.02))
        # xx, yy = xx.reshape((xx.size, 1)), yy.reshape((yy.size, 1))
        xdata = np.hstack((xx.reshape((xx.size, 1)), yy.reshape((yy.size, 1))))
        zz = cls.predict(xdata).reshape(xx.shape)

        plt.contour(xx, yy, zz, levels=[0],
                    colors=['k'], linestyles=['-'])
        if disp_options[0] in display:
            zp = np.ones(zz.shape)
            zp[zz < 0] = -1

            plt.contourf(xx, yy, zp, 10, alpha=0.2, colors=['r', 'b'])
        if disp_options[1] in display:
            zf = cls.decision_function(xdata).reshape(xx.shape)
            ct = plt.contour(xx, yy, zf, levels=[-1, 0, 1],
                             colors=['k'], linestyles=['--', '-', '--'])
        if disp_options[2] in display:
            svec = cls.support_vectors_
            plt.scatter(svec[:, 0], svec[:, 1],
                        marker='o', color='None', s=150, linewidth=1.5, edgecolor='k')

    elif pred_model == models[5]:
        expd = st.expander('Model and display options', expanded=False)
        with expd:
            k_value = st.slider(label='Number of near neighbors',
                                min_value=1, max_value=15, value=5, step=2)
            disp_options = ['Prediction']
            display = st.multiselect(label='Display options',
                                     options=disp_options)

        cls = KNeighborsClassifier(n_neighbors=k_value)
        cls.fit(x, y)

        xx, yy = np.meshgrid(np.arange(-3, 5.55, 0.05),
                             np.arange(-3, 5.55, 0.05))
        xdata = np.hstack((xx.reshape((xx.size, 1)), yy.reshape((yy.size, 1))))
        zz = cls.predict(xdata).reshape(xx.shape)

        plt.contour(xx, yy, zz, levels=[0],
                    colors=['k'], linestyles=['-'])

        if disp_options[0] in display:
            plt.contourf(xx, yy, zz, 10, alpha=0.2, colors=['r', 'b'])

    if pred_model == models[0]:
        class1_label = 'Class 1'
        class2_label = 'Class 2'
        pred_model = 'Simulated data'
    else:
        y_pred = cls.predict(x)
        if pred_model == models[1]:
            y_pred = 2*y_pred - 1

        class1_pa = ((y_pred == -1)&(y == -1)).sum() / 30
        class2_pa = ((y_pred == 1)&(y == 1)).sum() / 30

        class1_label = 'Class 1: training accuracy: {0:.3f}'.format(class1_pa)
        class2_label = 'Class 2: training accuracy: {0:.3f}'.format(class2_pa)

    plt.scatter(x[y==-1, 0], x[y==-1, 1], c='r', alpha=0.4, label=class1_label)
    plt.scatter(x[y==1, 0], x[y==1, 1], c='b', alpha=0.4, label=class2_label)

    plt.legend(fontsize=11, loc='upper left', bbox_to_anchor=[1., 1.028])
    plt.axis('equal')
    plt.xlim([-2.7, 5.3])
    plt.ylim([-2.7, 5.3])
    plt.xticks(np.arange(-2, 6))
    plt.yticks(np.arange(-2, 6))
    plt.xlabel('Predictor variable $x_1$', fontsize=12)
    plt.ylabel('Preidctor varaible $x_2$', fontsize=12)
    plt.title(pred_model, fontsize=14)

    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.image(buf)



# @st.cache
# def slr_data():

#     n = 20
#     x_i = rd.rand(n)
#     x_i.sort()
#     u_i = rd.normal(size=n)
#     y_i = beta0 + beta1*x_i + u_i
#     data = pd.DataFrame(np.vstack((y_i, x_i)).T, columns=['y', 'x'])

#     return data



#@st.cache
@st.experimental_memo
def xydata(beta0, beta1, n, refresh=True):

    xi = rd.rand(n)
    xi.sort()
    ui = rd.normal(size=n)
    yi = beta0 + beta1*xi + ui
    data = pd.DataFrame(np.vstack((yi, xi)).T, columns=['y', 'x'])

    return data


@st.cache
def two_class_data(n, separable):

    if separable == 'Separable':
        x = 1 - 3*rd.rand(2*n, 2)
        y = np.array([-1]*n + [1]*n)
        x[y==1, 0] += 4
        x[y==1, 1] += 3

    elif separable == 'Barely separable':
        x = rd.normal(size=(2*n, 2))
        y = np.array([-1]*n + [1]*n)
        x[y==1, :] += 1.5
        x += 0.3

    elif separable == 'Non-separable':
        x = 0.6*rd.normal(size=(2*n, 2))
        y = np.array([-1]*n + [1]*n)
        x[:n//2, :] += 3
        x[n//2:n, :] -= 0.5
        x[-n:, :] += 1.5

    return x, y


if __name__ == "__main__":
    main()
