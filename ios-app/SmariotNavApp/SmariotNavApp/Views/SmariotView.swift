//
//  SmariotView.swift
//  SmariotNavApp
//
//  Created by Heidi Albarazi on 16.06.24.
//



import SplineRuntime
import SwiftUI

struct SmariotView: View {
    var body: some View {
        // fetching from cloud
        let url = URL(string: "https://build.spline.design/0OIOPtsz3BfVl41VfsYI/scene.splineswift")!

        // // fetching from local
        // let url = Bundle.main.url(forResource: "scene", withExtension: "splineswift")!

        SplineView(sceneFileURL: url).ignoresSafeArea(.all)
    }
}

#Preview {
    SmariotView()
}
