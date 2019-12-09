//
//  Coordinate.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/18/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import CoreLocation

/// Represents a Coordinate.
struct Coordinate: Hashable {
    /// The latitude of the point.
    var latitude: Double
    /// The longitude of the point.
    var longitude: Double
    
    /// The `CoreLocation` representation of the object.
    var locationCoordinate : CLLocationCoordinate2D {
        return CLLocationCoordinate2D(latitude: latitude, longitude: longitude)
    }
}
