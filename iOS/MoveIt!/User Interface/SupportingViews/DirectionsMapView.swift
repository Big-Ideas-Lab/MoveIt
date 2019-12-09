//
//  DirectionsMapView.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/8/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import MapKit

struct DirectionsMapView: UIViewRepresentable {
    @Binding var directions: MKDirections?
    
    func makeCoordinator() -> Coordinator {
        return Coordinator(self)
    }
    
    func makeUIView(context: UIViewRepresentableContext<DirectionsMapView>) -> MKMapView {
        let mapView = MKMapView(frame: .zero)
        mapView.delegate = context.coordinator
        mapView.isUserInteractionEnabled = false
        mapView.showsUserLocation = true
        return mapView
    }
    
    func updateUIView(_ mapView: MKMapView, context: UIViewRepresentableContext<DirectionsMapView>) {
        directions?.calculate { response, error in
            guard let unwrappedResponse = response else { return }

            for route in unwrappedResponse.routes {
                mapView.addOverlay(route.polyline)
                mapView.setVisibleMapRect(route.polyline.boundingMapRect.insetBy(dx: -10000, dy: -10000), animated: true)
            }
        }
    }
    
    class Coordinator: NSObject, MKMapViewDelegate {
        var parent: DirectionsMapView

        init(_ mapView: DirectionsMapView) {
            self.parent = mapView
        }
        
        func mapView(_ mapView: MKMapView, rendererFor overlay: MKOverlay) -> MKOverlayRenderer {
            let renderer = MKPolylineRenderer(polyline: overlay as! MKPolyline)
            renderer.strokeColor = .blue
            return renderer
        }
    }
}

//struct DirectionsMapView_Previews: PreviewProvider {
//    static var previews: some View {
//        DirectionsMapView()
//    }
//}
