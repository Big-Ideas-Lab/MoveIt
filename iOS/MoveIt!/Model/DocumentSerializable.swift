//
//  DocumentSerializable.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/15/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import Foundation

/// Represents a type that can be instantiated from a Firebase Document.
protocol DocumentSerializable {
    /// Initializes the conforming type based on a Firebase Document.
    /// - Parameter dictionary: The dictionary to initialize from.
    init?(dictionary: [String: Any])
}
