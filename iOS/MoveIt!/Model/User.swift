//
//  User.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/30/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI

class User: ObservableObject {
    @Published var id: String
    @Published var displayName: String?
    @Published var photoURL: URL?
    @Published var email: String?
    @Published var phoneNumber: String?
    
    init(id: String, displayName: String? = nil, photoURL: URL? = nil, email: String? = nil, phoneNumber: String? = nil) {
        self.id = id
        self.displayName = displayName
        self.photoURL = photoURL
        self.email = email
        self.phoneNumber = phoneNumber
    }
}
