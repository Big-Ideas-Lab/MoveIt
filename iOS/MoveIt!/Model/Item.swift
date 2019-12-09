//
//  Item.swift
//  MoveIt!
//
//  Created by MoveIt on 9/19/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import FirebaseFirestore
import CoreLocation

/// Represents a menu item that a user can purchase from a restaurant.
struct Item: Identifiable, Hashable {
    /// The id of this item.
    var id: String
    /// The price of the item.
    var price: Double
    /// The name of the item.
    var name: String
    /// The confidence that the user will choose the item.
    var confidenceScore: Double
    /// The score that represents how healthy the item is.
    var healthScore: Double
    /// The location of the restaurant.
    var location: Coordinate
    /// The name of the restaurant.
    var restaurantName: String
}

// MARK: - DictionaryCodable
extension Item : DictionaryCodable {
    init?(dictionary: [String : Any]) {
        guard let id = dictionary["id"] as? String,
        let price = dictionary["price"] as? Double,
        let name = dictionary["item"] as? String,
        let confidenceScore = dictionary["confidenceScore"] as? Double,
        let healthScore = dictionary["healthScore"] as? Double,
        let location = dictionary["location"] as? GeoPoint,
        let restaurantName = dictionary["restName"] as? String else { return nil }
        
        self.id = id
        self.price = price
        self.name = name
        self.confidenceScore = confidenceScore
        self.healthScore = healthScore
        self.location = location.coordinates
        self.restaurantName = restaurantName
    }
    
    var dictionary: [String: Any] {
        return [
            "id": id,
            "price": price,
            "name": name,
            "confidenceScore": confidenceScore,
            "healthScore": healthScore,
            "location": location,
            "restaurantName": restaurantName
        ]
    }
}
