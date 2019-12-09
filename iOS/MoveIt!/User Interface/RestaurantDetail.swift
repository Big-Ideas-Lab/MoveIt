//
//  RestaurantDetail.swift
//  MoveIt!
//
//  Created by MoveIt on 9/19/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import MapKit

struct RestaurantDetail: View {
    var item: Item
    var onDismiss: () -> ()
    @State var currentLocation: CLLocation = CLLocation(latitude: 0, longitude: 0)
    @State var directions: MKDirections?
    
    var body: some View {
        ZStack(alignment: .bottom) {
            DirectionsMapView(directions: $directions).onAppear(perform: computeDirections)
            VStack {
                Button(action: {
                    let mapItem = MKMapItem(placemark: MKPlacemark(coordinate: self.item.location.locationCoordinate, addressDictionary: nil))
                    mapItem.openInMaps()
                }, label: {
                    Text("Open in Apple Maps")
                    .padding()
                    .background(Color.blue)
                    .foregroundColor(Color.white)
                    .cornerRadius(15)
                    .font(.headline)
                })
            }
        }
    }
    
    func computeDirections() {
        let request = MKDirections.Request()
        let locationManager = MILocationManager()
        currentLocation = locationManager.locationManager.location ?? CLLocation(latitude: 0, longitude: 0)
        locationManager.locationWasUpdatedCompletion = { self.currentLocation = $0 }
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: currentLocation.coordinate, addressDictionary: nil))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: item.location.locationCoordinate, addressDictionary: nil))
        request.transportType = .walking

        let directions = MKDirections(request: request)
        self.directions = directions
    }
}

//struct RestaurantDetail_Previews: PreviewProvider {
//    static var previews: some View {
//        RestaurantDetail(item: Restraunt, onDismiss: <#T##() -> ()#>)
//    }
//}
