ListView {
    id: topicListView
    Layout.fillWidth: true
    Layout.fillHeight: true
    model: topicModel
    spacing: 12
    clip: true

    delegate: Rectangle {
        width: topicListView.width
        height: 70
        color: "#2a2a2a"
        radius: 8
        border.width: 2
        border.color: {
            if (model.status === "Receiving") return "#00cc66"
            else if (model.status === "No Data") return "#ff9933"
            else return "#cc0000"
        }

        RowLayout {
            anchors.fill: parent
            anchors.margins: 15
            spacing: 15

            // Status LED indicator
            Rectangle {
                width: 24
                height: 24
                radius: 12
                color: {
                    if (model.status === "Receiving") return "#00ff66"
                    else if (model.status === "No Data") return "#ffaa00"
                    else return "#ff3333"
                }
                
                // Pulsing animation for active topics
                SequentialAnimation on opacity {
                    running: model.status === "Receiving"
                    loops: Animation.Infinite
                    NumberAnimation { from: 1.0; to: 0.3; duration: 800 }
                    NumberAnimation { from: 0.3; to: 1.0; duration: 800 }
                }
                
                Layout.alignment: Qt.AlignVCenter
            }

            // Text content
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4

                // System name (alias) - large and prominent
                Text {
                    text: model.alias
                    font.pointSize: 14
                    font.bold: true
                    color: "#ffffff"
                    Layout.fillWidth: true
                    elide: Text.ElideRight
                }

                // Topic name - smaller, secondary
                Text {
                    text: model.topic
                    font.pointSize: 10
                    color: "#888888"
                    font.family: "monospace"
                    Layout.fillWidth: true
                    elide: Text.ElideMiddle
                }
            }

            // Status text - large and clear
            Rectangle {
                Layout.preferredWidth: 120
                height: 40
                radius: 6
                color: {
                    if (model.status === "Receiving") return "#003322"
                    else if (model.status === "No Data") return "#332200"
                    else return "#330000"
                }

                Text {
                    anchors.centerIn: parent
                    text: model.status.toUpperCase()
                    font.pointSize: 11
                    font.bold: true
                    color: {
                        if (model.status === "Receiving") return "#00ff66"
                        else if (model.status === "No Data") return "#ffaa00"
                        else return "#ff6666"
                    }
                }
            }
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: parent.color = "#333333"
            onExited: parent.color = "#2a2a2a"
        }
    }

    ScrollBar.vertical: ScrollBar {
        policy: ScrollBar.AsNeeded
        width: 10
        
        contentItem: Rectangle {
            radius: 5
            color: "#555555"
        }
    }
}
