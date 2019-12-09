//
//  MIAuthenticationManager.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/28/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import FirebaseUI

class MIAuthenticationManager: NSObject, FUIAuthDelegate {
    var loginCompletion: (User?, Error?) -> Void
    
    init(loginCompletion: @escaping (User?, Error?) -> Void) {
        self.loginCompletion = loginCompletion
    }
    
    func createAuthUI() -> FUIAuth? {
        let authUI = FUIAuth.defaultAuthUI()
        let providers: [FUIAuthProvider] = [
          FUIGoogleAuth(),
          FUIEmailAuth()
        ]
        authUI?.providers = providers
        authUI?.delegate = self
        return authUI
    }
    
    func authUI(_ authUI: FUIAuth, didSignInWith authDataResult: AuthDataResult?, error: Error?) {
        guard let firebaseUser = authDataResult?.user else { return }
        let user = User(id: firebaseUser.uid, displayName: firebaseUser.displayName, photoURL: firebaseUser.photoURL, email: firebaseUser.email, phoneNumber: firebaseUser.phoneNumber)
        loginCompletion(user, error)
    }
}
