#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QtGui>
#include <QtCore>
#include <vector>
using namespace std;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
public slots:
    void Mouse_Pressed();
    void showMousePosition(QPoint& pos);
public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void on_show_axes_clicked();

    void on_Draw_clicked();

    void on_set_point1_clicked();

    void on_set_point2_clicked();

    void on_resetButton_clicked();

    void on_setgridbutton_clicked();

    void delay();

    void on_DDALine_clicked();

    void on_bresenhamLine_clicked();

    void on_bresenhamCircle_clicked();

    void on_clearButton_clicked();

    void on_polarCircle_clicked();

    void on_polarEllipse_clicked();

    void on_midpointEllipse_clicked();

    void on_boundaryFill_clicked();

    void on_floodFill_clicked();

    void on_setPolygonVertex_clicked();

    void on_clearPolygonVertex_clicked();

    void on_scanlineFill_clicked();

    void on_translation_clicked();

    void on_scaling_clicked();

    void on_shearing_clicked();

    void on_rotation_clicked();

    void on_reflection_clicked();

    void on_setcorner1_clicked();

    void on_setcorner2_clicked();

    void on_lineclipping_clicked();

    void on_polygonclipping_clicked();

private:
    Ui::MainWindow *ui;
    QPoint p1,p2;
    QPoint cp1,cp2;
    void point(int,int,int,int,int);
    void DDAline(int, int, int);
    void boundaryFillutil(int, int, QRgb, int, int, int);
    void floodFillutil(int, int, QRgb, int, int, int);
    void initEdgeTable();
    void storeEdgeInTable(int, int, int, int);
    void poly_draw(vector<pair<int,int>>, int, int, int);
    void draw_Window();
    int computeCode(int, int);
    void cohenSutherlandClip(int, int, int, int);
    int x_intersect(int, int, int, int, int, int, int, int);
    int y_intersect(int, int, int, int, int, int, int, int);
    void clip(int, int, int, int);
    void suthHodgClip();
};

#endif // MAINWINDOW_H
