//
//  MIHealthKitManager.swift
//  MoveIt!
//
//  Created by Harish Yerra on 10/25/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import HealthKit

class MIHealthKitManager: NSObject {
    
    let healthStore = HKHealthStore()
    static let shared = MIHealthKitManager()
    
    enum HealthType: CaseIterable {
        case stepCount
        
        var objectType: HKObjectType {
            switch self {
            case .stepCount:
                return HKObjectType.quantityType(forIdentifier: .stepCount)!
            }
        }
        
        var quantityType: HKQuantityType {
            switch self {
            case .stepCount:
                return HKQuantityType.quantityType(forIdentifier: .stepCount)!
            }
        }
    }
    
    enum Duration {
        case daily
        case weekly
    }
    
    func requestPermission(for types: [HealthType]) {
        let healthTypes = Set(types.map { return $0.objectType })
        healthStore.getRequestStatusForAuthorization(toShare: [], read: healthTypes) { status, error in
            if status == .shouldRequest {
                self.healthStore.requestAuthorization(toShare: nil, read: healthTypes) { success, error in
                    // TODO: Perform error handling
                }
            }
        }
    }
    
    func retrieve(_ healthType: HealthType, during: Duration, completion: @escaping (Double) -> Void) {
        requestPermission(for: [healthType])
        let type = healthType.quantityType
            
        let now = Date()
        guard let anchorDate = during == .daily ? Calendar.current.startOfDay(for: now) : Calendar.current.date(byAdding: .weekOfYear, value: -1, to: Date()) else { return }
        var interval = DateComponents()
        switch during {
        case .daily: interval.day = 1
        case .weekly: interval.weekOfYear = 1
        }
        
        let query = HKStatisticsCollectionQuery(quantityType: type,
                                                quantitySamplePredicate: nil,
                                                options: [.cumulativeSum],
                                                anchorDate: anchorDate,
                                                intervalComponents: interval)
        query.initialResultsHandler = { _, result, error in
            // TODO: Perform error handling
            var resultCount = 0.0
            result?.enumerateStatistics(from: anchorDate, to: now) { statistics, _ in
                guard let sum = statistics.sumQuantity() else { return }
                resultCount = sum.doubleValue(for: HKUnit.count())
                DispatchQueue.main.async { completion(resultCount) }
            }
            
        }
        query.statisticsUpdateHandler = {
            query, statistics, statisticsCollection, error in
            
            // If new statistics are available
            if let sum = statistics?.sumQuantity() {
                let resultCount = sum.doubleValue(for: HKUnit.count())
                DispatchQueue.main.async { completion(resultCount) }
            }
        }
        
        healthStore.execute(query)
    }
    
}
