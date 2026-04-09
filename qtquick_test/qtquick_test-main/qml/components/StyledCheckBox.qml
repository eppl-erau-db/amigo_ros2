CheckBox {
    id: cbx
    property string iconSymbol: "🗺️" // default emoji
    font.pointSize: 11
    spacing: 10

    indicator: Rectangle {
        width: 20
        height: 20
        radius: 4
        border.width: 2
        border.color: cbx.checked ? "#00cc66" : "#666"
        color: cbx.checked ? "#003318" : "#222"
        Behavior on border.color { ColorAnimation { duration: 120 } }
        Behavior on color       { ColorAnimation { duration: 120 } }

        // checkmark
        Text {
            anchors.centerIn: parent
            visible: cbx.checked
            text: "✓"
            color: "#00ff88"
            font.bold: true
            font.pointSize: 14
        }
    }

    contentItem: Row {
        spacing: 10
        Text {
            text: cbx.iconSymbol
            font.pointSize: 14
            color: cbx.checked ? "#00ff88" : "#bbbbbb"
        }
        Text {
            text: cbx.text
            color: "#eeeeee"
            font.pointSize: 12
        }
    }

    // Hover effect
    Rectangle {
        anchors.fill: parent
        color: "transparent"
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: parent.color = "#222228"
            onExited: parent.color = "transparent"
        }
    }
}