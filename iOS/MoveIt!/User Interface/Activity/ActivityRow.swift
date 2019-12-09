//
//  ActivityRow.swift
//  MoveIt!
//
//  Created by MoveIt on 9/19/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import HealthKit
import HealthKitUI

struct ActivityRow: View {
    @ObservedObject var dailyStepCount = StepCount(steps: nil, duration: .daily)
    @ObservedObject var weeklyStepCount = StepCount(steps: nil, duration: .weekly)
    
    var body: some View {
        VStack(alignment: .leading) {
            Text(verbatim: "Activity")
                .font(.title)
                .fontWeight(.heavy)
            StepCountRow(stepCount: dailyStepCount)
            StepCountRow(stepCount: weeklyStepCount)
        }.onAppear(perform: displaySteps)
    }
    
    func displaySteps() {
        MIHealthKitManager.shared.retrieve(.stepCount, during: .daily) { result in
            self.dailyStepCount.steps = result
        }
        MIHealthKitManager.shared.retrieve(.stepCount, during: .weekly) { result in
            self.weeklyStepCount.steps = result
        }
    }
}

struct ActivityRow_Previews: PreviewProvider {
    static var previews: some View {
        ActivityRow()
    }
}
