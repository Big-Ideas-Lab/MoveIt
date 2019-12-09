//
//  ExerciseRow.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/18/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import FirebaseFirestore

struct ExerciseRow: View {
    @ObservedObject var walksCollection = LiveCollection<Walk>(query: Firestore.firestore().collection("Users").document("User0").collection("walk_recs"))
    
    var body: some View {
        VStack(alignment: .leading) {
            Text("Exercise")
                .font(.title)
                .fontWeight(.heavy)
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(alignment: .top, spacing: 0) {
                    ForEach(self.walksCollection.items) { walk in
                        NavigationLink(destination: WalkDetail()) {
                            WalkItem(item: walk)
                        }
                    }
                }
            }
            .frame(height: 250)
        }
    }
}

struct WalkItem: View {
    var item: Walk
    let width: CGFloat = 250.0
    let height: CGFloat = 200.0
    
    let colors: [Color] = [Color.gray.opacity(0.5), Color.gray.opacity(0.3)]

    
    var gradient: LinearGradient {
        LinearGradient(gradient: Gradient(colors: colors),
                       startPoint: .top, endPoint: .bottom)
    }
    
    var body: some View {
        ZStack(alignment: Alignment.topLeading) {
            MapView(coordinate: item.beginningLocation.locationCoordinate, animate: false, mapType: .satellite)
                .frame(width: width, height: height)
                .cornerRadius(5.0)
            Rectangle().frame(width: width, height: height).opacity(0)
            Rectangle().fill(gradient).cornerRadius(8)
                .frame(width: width*3/4, height: height*2/4)
                .padding(.top, height/4)
                .padding(.leading, 15)
            Text(item.name).bold()
                .foregroundColor(.primary)
                .font(.caption)
                .padding(.top, 15)
                .padding(.leading, 15)
                
        }
        .padding(.leading, 15)
        .padding(.bottom, 30)
    }
}

struct ExerciseRow_Previews: PreviewProvider {
    static var previews: some View {
        ExerciseRow()
    }
}
