//
//  GeoPoint+CoreLocation.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/15/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import FirebaseFirestore
import CoreLocation

// MARK: - Core Location
extension GeoPoint {
    /// Returns the `CLLocationCoordinate2D` representation of `GeoPoint`.
    var coordinate2D: CLLocationCoordinate2D {
        return CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }
    
    /// Returns the `Coordinates` representation of GeoPoint.
    var coordinates: Coordinate {
        return Coordinate(latitude: latitude, longitude: longitude)
    }
}
