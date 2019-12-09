//
//  MILocationManager.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/8/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import CoreLocation

class MILocationManager: NSObject, CLLocationManagerDelegate {
    var locationManager = CLLocationManager()
    var locationWasUpdatedCompletion: ((CLLocation) -> Void)?
    
    override init() {
        locationManager.requestAlwaysAuthorization()
        locationManager.startUpdatingLocation()
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation]) {
        locationWasUpdatedCompletion?(locations.last!)
    }
}
