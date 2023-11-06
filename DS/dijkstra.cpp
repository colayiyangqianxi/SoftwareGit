#include <iostream>
#include <string>

using namespace std;
const int Big = 1000;

class WebPage
{
public:
    int n;             // n个结点
    string graph[10];  //顶点数组
    float Eff[10][10]; //邻接矩阵，初始输入效率矩阵
    void Enter()
    {
        n = 10;
        for (int i = 0; i < n; i++)
        {
            cin >> graph[i]; //输入n个结点
        }
        int i, j;
        for (i = 0; i < n; i++)
        {
            for (j = 0; j < n; j++)
            {
                cin >> Eff[i][j]; //输入各网页间跳转效率
            }
        }
    }

    //两个查找函数find1&find2
    int find1(string s_) //字符找下标
    {
        for (int a = 0; a < n; a++)
        {
            if (graph[a] == s_)
            {
                return a;
            }
        }
    }
    string find2(int i) //下标找字符
    {
        for (int a = 0; a < n; a++)
        {
            if (a == i)
            {
                return graph[a];
            }
        }
    }

    void dijkstra(string page) // page为网页1,由此开始查找最短跳转路径
    {
        float *dis = new float[n];    //最短距离
        int *Visit = new int[n];      //记录访问数组
        string *road = new string[n]; //最优路径
        int i, j, k;
        for (k = 0; k < n; k++)
        {
            Visit[k] = 0;                     //每一次都重新初始化访问状态visit
            road[k] = page + "->";            //路径起点为网页1(page)
            dis[k] = 1 / Eff[find1(page)][k]; //以page为起点,遍历page到剩余9个网页(pagex)的距离(不经过其它网页的前提下)
        }
        Visit[find1(page)] = 1; //网页到自身无意义 记为已访问过
        float min;              //路径最小值

        for (k = 0; k < n; k++)
        {                  //从page开始对除了page之外的n9个网页分别进行循环遍历
            min = Big;     //先令最小值无限大
            int flag = -1; // flag为网页(pagex)下标 对page来说，哪个网页(pagex)与其(即page)距离最近
            for (i = 0; i < n; i++)
            {
                if (Visit[i] == 0)
                { //若此网页(pagex)未被访问
                    if (dis[i] < min)
                    {                 //且是距离上一个点距离最小的点
                        flag = i;     //标记此点
                        min = dis[i]; //更新最短距离(此时min是从(page->pagex)的min，即已加上前面所有部分)
                    }
                }
            }

            if (flag != -1)
            {                                          //此判断 防止flag没有变化(即page到不了某网页(本例为到自身无意义)，防止此pagex进入 导致溢出或无意义操作)
                road[flag] = road[flag] + find2(flag); //线路更新递加;已有路径(road[flag])+新进入路径(Pagex) 是字符串的直接相加(进入方式)
                Visit[flag] = 1;                       //表示此pagex(flag)已被访问过了
                for (j = 0; j < n; j++)
                {
                    if ((Visit[j] == 0) && (min + 1 / Eff[flag][j] < dis[j]))
                    {                                    //从flag(pagex)出发，下一个pagex未被访问；且最短距离: page->flag(pagex)->j(pagex)  <  page->j(pagex)
                        dis[j] = min + 1 / Eff[flag][j]; //更新 更短路径(dis始终记录page->pagej(pagex)的最短距离)
                        road[j] = road[flag] + "->";     //更新 路径字符串road[j]即为road[flag]字符串
                    }
                }
            }
        }

        for (int i = 0; i < n; i++)
        {
            if (i != find1(page)) //网页与自身距离无意义 排除
            {
                cout << "网页1:" << page << " 网页2:" << find2(i) << " 最短跳转距离:" << dis[i] << " 最优跳转路径:" << road[i] << endl;
            }
        }
    }
    void Print()
    {
        for (int i = 0; i < 10; i++)
        {
            dijkstra(graph[i]); //分别遍历10个网页间最短距离
            cout << endl;
        }
    }
};
int main()
{
    WebPage wpage; //定义网页类
    wpage.Enter(); //输入10个网页间的跳转效率
    wpage.Print(); //输出最短距离及最优路径
    return 0;
}