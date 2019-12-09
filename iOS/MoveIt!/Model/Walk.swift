//
//  Walk.swift
//  MoveIt!
//
//  Created by MoveIt on 9/20/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import Foundation
import FirebaseFirestore

/// Represents a walk that a user can take.
struct Walk: Hashable, Identifiable {
    /// The `id` of the walk.
    var id: String
    /// The name of the location of the walk.
    var name: String
    /// The starting location of the walk.
    var beginningLocation: Coordinate
    /// The end location of the walk.
    var endLocation: Coordinate
    /// The confidence that the user will take or enjoy this walk.
    var confidenceScore: Double
}

// MARK: - DictionaryCodable
extension Walk: DictionaryCodable {
    init?(dictionary: [String : Any]) {
        guard let id = dictionary["id"] as? String,
        let name = dictionary["name"] as? String,
        let beginningLocation = dictionary["beginning_location"] as? GeoPoint,
        let endLocation = dictionary["end_location"] as? GeoPoint,
        let confidenceScore = dictionary["confidence_score"] as? Double else { return nil }
        
        self.id = id
        self.name = name
        self.beginningLocation = beginningLocation.coordinates
        self.endLocation = endLocation.coordinates
        self.confidenceScore = confidenceScore
    }
    
    var dictionary: [String : Any] {
        return [
            "id": id,
            "name": name,
            "beginning_location": beginningLocation,
            "end_location": endLocation,
            "confidence_score": confidenceScore
        ]
    }
}
