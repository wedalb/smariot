
//
//  MainView.swift
//  testo
//
//  Created by Heidi Albarazi on 28.05.24.
//

import SwiftUI

/// This View is the main view that controlls all other views and also contains the tabbar.
struct MainView: View {
    
    init() {
    UITabBar.appearance().backgroundColor = UIColor.white
    }

    var body: some View {
        TabView {
            ARContentView()
                .tabItem {
                    Label("AR View", systemImage: "arkit")
                }

            SettingsView()
                .tabItem {
                    Label("Hello", systemImage: "globe")
                }
            SmariotView()
                .tabItem{
                    Label("Smariot", systemImage: "globe")
                }
        }
    }
}

struct MainView_Previews: PreviewProvider {
    static var previews: some View {
        MainView()
    }
}
