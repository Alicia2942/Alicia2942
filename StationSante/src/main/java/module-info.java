module com.isen.stationsante {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.base;

    opens com.isen.stationsante to javafx.fxml;
    exports com.isen.stationsante;
    requires javafx.graphicsEmpty;
}
