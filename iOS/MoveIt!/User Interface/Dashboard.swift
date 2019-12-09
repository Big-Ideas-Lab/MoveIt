//
//  Dashboard.swift
//  MoveIt!
//
//  Created by MoveIt on 9/19/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import FirebaseUI

struct Dashboard: View {
    @EnvironmentObject var user: User
    var locationManager = MILocationManager()
    
    var body: some View {
        List {
            ActivityRow()
            NutritionRow()
            ExerciseRow()
        }
        .padding(.top)
    }
}

struct Dashboard_Previews: PreviewProvider {
    static var previews: some View {
        Dashboard()
    }
}
