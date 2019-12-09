//
//  DictionaryCodable.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/15/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import Foundation

/// Represents a type that can be instantiated from a Dictionary.
protocol DictionaryDecodable {
    /// Initializes the conforming type based on a Firebase Document.
    /// - Parameter dictionary: The dictionary to initialize from.
    init?(dictionary: [String: Any])
}

/// Represents a type that can be encoded into a Dictionary.
protocol DictionaryEncodable {
    /// The dictionary that the object was encoded into.
    var dictionary: [String: Any] { get }
}

typealias DictionaryCodable = DictionaryDecodable & DictionaryEncodable
