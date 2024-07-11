//
//  SettingsView.swift
//  SmariotNavApp
//
//  Created by Heidi Albarazi on 28.05.24.
//
import SwiftUI
import MapKit

struct SettingsView: View {
    @State private var searchText = ""
    @State private var destination: MKPlacemark?
    @State private var showMapView = false

    var body: some View {
        VStack(spacing: 20) {
            Text("Settings")
                .font(.title)
                .bold()
            
            TextField("Search", text: $searchText, onCommit: searchLocation)
                .padding()
                .background(Color.gray.opacity(0.2))
                .cornerRadius(10)
            
            Button(action: {
                setPredefinedLocation(name: "Home", latitude: 37.7749, longitude: -122.4194)
            }) {
                HStack {
                    Image(systemName: "house")
                    Text("Set Home")
                }
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
            }
            
            Button(action: {
                setPredefinedLocation(name: "Doctor", latitude: 37.7749, longitude: -122.4194)
            }) {
                HStack {
                    Image(systemName: "staroflife")
                    Text("Set Doctor")
                }
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(10)
            }
            
            HStack(spacing: 20) {
                Button(action: {
                    setPredefinedLocation(name: "Supermarket", latitude: 37.7749, longitude: -122.4194)
                }) {
                    Text("Supermarket")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                
                Button(action: {
                    setPredefinedLocation(name: "Garden", latitude: 37.7749, longitude: -122.4194)
                }) {
                    Text("Garden")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
        }
        .padding()
        .sheet(isPresented: $showMapView) {
            MapView(destination: $destination)
        }
    }
    
    private func searchLocation() {
        let searchRequest = MKLocalSearch.Request()
        searchRequest.naturalLanguageQuery = searchText
        let search = MKLocalSearch(request: searchRequest)
        search.start { response, error in
            guard let mapItem = response?.mapItems.first else { return }
            destination = mapItem.placemark
            showMapView = true
        }
    }
    
    private func setPredefinedLocation(name: String, latitude: CLLocationDegrees, longitude: CLLocationDegrees) {
        let placemark = MKPlacemark(coordinate: CLLocationCoordinate2D(latitude: latitude, longitude: longitude))
        destination = placemark
        showMapView = true
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
    }
}
