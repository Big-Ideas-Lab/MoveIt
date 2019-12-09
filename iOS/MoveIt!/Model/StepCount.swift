//
//  StepCount.swift
//  MoveIt!
//
//  Created by Harish Yerra on 10/30/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import Combine

class StepCount: ObservableObject {
    @Published var steps: Double?
    var duration: MIHealthKitManager.Duration
    
    init(steps: Double?, duration: MIHealthKitManager.Duration) {
        self.steps = steps
        self.duration = duration
    }
}
