import QtQuick 2.6
import QtQuick.Controls 2.0
Rectangle {
    id:window
    height:Screen.desktopAvailableHeight
    width:Screen.desktopAvailableWidth
    visible: true
    color: "#000000"
    objectName: "win"
    property double i: 0.0
    property bool timerRun: true
    signal closeme()
    FontLoader{
                id:hundergad
                source: "hundergad.ttf"
            }
    FontLoader{
                id:myFont
                source: "showhan.otf"
            }
    Timer{
        id:t1
        interval: 500
        repeat: true
        running: timerRun
        onTriggered: update()

    }

    function update()
    {
        i=i+0.1
        pb.value=i
        // console.log(pb.value)
        if(pb.value===0.9999999999999999 || pb.value===1.0)
           {
            t1.running=false
            pb.visible=false
            closeme()
        }


    }

    ProgressBar {
        id: pb
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        width: 400
        height: 29
        visible: true
    }

    Label {
        id: label
        width: 591
        height: 95
        visible: true
        color: "#7aacde"
        text: qsTr("Silver Scissors")
        anchors.top: parent.top
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.topMargin: 252
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: myFont.name
        font.bold: true
        font.pointSize: 42
    }


    Label {
        id: label2
        x: 1136
        y: 761
        width: 400
        height: 55
        color: "#817474"
        text: qsTr("Developed By : @lucifer_codes")
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        font.pointSize: 20
        font.bold: true
    }

    Label {
        id: label1
        y: 485
        width: 429
        height: 62
        property int i
                property bool isTag
                property string sourceText: "Loading..."

                function type() {
                    text = sourceText.slice(0, ++i);
                    if (text === sourceText) return timer.stop()

                    label1.text = text;
                }

        color: "#ffffff"
        anchors.bottom: parent.bottom
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        font.family: hundergad.name
        font.pointSize: 40
        font.bold: true
        anchors.horizontalCenterOffset: 0
        anchors.bottomMargin: 269
        anchors.horizontalCenter: parent.horizontalCenter

    }
}







