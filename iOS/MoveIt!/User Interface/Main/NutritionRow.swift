//
//  NutritionRow.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/18/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI
import FirebaseFirestore
import MapKit

struct NutritionRow: View {
    @ObservedObject var restaurantsCollection = LiveCollection<Item>(query: Firestore.firestore().collection("Users").document("User0").collection("rec1"))
    
    var body: some View {
        VStack(alignment: .leading) {
            Text("Nutrition")
                .font(.title)
                .fontWeight(.heavy)
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(alignment: .top, spacing: 0) {
                    ForEach(self.restaurantsCollection.items) { restaurant in
                        Button(action: {
                            let mapItem = MKMapItem(placemark: MKPlacemark(coordinate: restaurant.location.locationCoordinate, addressDictionary: nil))
                            mapItem.openInMaps()
                        }) {
                            RestaurantItem(item: restaurant)
                        }
                    }
                }
            }
            .frame(height: 250)
        }
    }
}

struct RestaurantItem: View {
    var item: Item
    let width: CGFloat = 250.0
    let height: CGFloat = 200.0
    
    let colors: [Color] = [Color.gray.opacity(0.5), Color.gray.opacity(0.3)]

    
    var gradient: LinearGradient {
        LinearGradient(gradient: Gradient(colors: colors),
                       startPoint: .top, endPoint: .bottom)
    }
    
    var body: some View {
        ZStack(alignment: .topLeading) {
            MapView(coordinate: item.location.locationCoordinate, animate: false)
                .frame(width: width, height: height)
                .cornerRadius(5.0)
            ZStack(alignment: .topLeading) {
                Rectangle().frame(width: width, height: height).opacity(0)
                Rectangle().fill(gradient).cornerRadius(8)
                    .frame(width: width*3/4, height: height*2/4)
                    .padding(.top, height/4)
                    .padding(.leading, 15)
            }
            Text(item.name).bold()
                .foregroundColor(.primary)
                .font(.caption)
                .font(.system(size: 20))
                .padding(.top, 15)
                .padding(.leading, 15)
        }
        .padding(.leading, 15)
        .padding(.bottom, 30)
    }
}

struct NutritionRow_Previews: PreviewProvider {
    static var previews: some View {
        NutritionRow()
    }
}
