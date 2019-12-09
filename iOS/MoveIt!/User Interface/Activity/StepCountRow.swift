//
//  StepCountRow.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/1/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI

struct StepCountRow: View {
    @ObservedObject var stepCount: StepCount
    
    var body: some View {
        switch stepCount.duration {
        case .daily:
            return VStack(alignment: .leading) {
                Text("Steps (Today)")
                HStack {
                    ProgressBar(progress: .constant(stepCount.steps ?? 0/10000)) // TODO: Replace 10000 with actual goal.
                    if stepCount.steps != nil {
                        Text("\(Int(stepCount.steps!)) / \(10000)") // TODO: Replace 10000 with actual goal.
                    }
                }
            }
        case .weekly:
            return VStack(alignment: .leading) {
                Text("Steps (This Week)")
                HStack {
                    ProgressBar(progress: .constant(stepCount.steps ?? 0/100000)) // TODO: Replace 100000 with actual goal.
                    if stepCount.steps != nil {
                        Text("\(Int(stepCount.steps!)) / \(100000)") // TODO: Replace 100000 with actual goal.
                    }
                }
            }
        }
    }
}

struct StepCountRow_Previews: PreviewProvider {
    static var previews: some View {
        StepCountRow(stepCount: StepCount(steps: 1500, duration: .daily))
    }
}
