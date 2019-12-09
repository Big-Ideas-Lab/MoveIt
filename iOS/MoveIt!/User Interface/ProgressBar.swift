//
//  ProgressBar.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/1/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import SwiftUI

struct ProgressBar: View {
    @Binding var progress: Double
    
    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: Alignment.leading) {
                Rectangle()
                    .foregroundColor(.gray)
                    .opacity(0.3)
                Rectangle()
                    .frame(minWidth: CGFloat(0), idealWidth: self.computeProgressBarWidth(geometry: geometry),
                           maxWidth: self.computeProgressBarWidth(geometry: geometry))
                    .animation(.default)
                    .opacity(0.6)
                    .foregroundColor(.orange)
            }
            .cornerRadius(5)
            .frame(height: 10)
        }
    }
    
    func computeProgressBarWidth(geometry: GeometryProxy) -> CGFloat {
        let frame = geometry.frame(in: .global)
        return frame.size.width * CGFloat(progress)
    }
    
}

struct ProgressBar_Previews: PreviewProvider {
    static var previews: some View {
        ProgressBar(progress: .constant(0.85))
    }
}
