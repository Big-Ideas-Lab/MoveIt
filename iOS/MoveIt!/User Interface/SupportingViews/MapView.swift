//
//  MapView.swift
//  MoveIt!
//
//  Created by MoveIt on 9/19/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import MapKit

struct MapView: UIViewRepresentable {
    var coordinate: CLLocationCoordinate2D
    var animate: Bool
    var mapType: MKMapType = .standard

    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView(frame: .zero)
        mapView.isUserInteractionEnabled = false
        mapView.mapType = mapType
        return mapView
    }

    func updateUIView(_ view: MKMapView, context: Context) {
        let span = MKCoordinateSpan(latitudeDelta: 0.02, longitudeDelta: 0.02)
        let region = MKCoordinateRegion(center: coordinate, span: span)
        view.setRegion(region, animated: animate)
    }
}

struct MapView_Previews: PreviewProvider {
    static var previews: some View {
        MapView(coordinate: CLLocationCoordinate2D(latitude: 180, longitude: 240), animate: false)
    }
}
