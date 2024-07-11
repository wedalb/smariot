//
//  RouteView.swift
//  SmariotNavApp
//
//  Created by Heidi Albarazi on 02.05.24.
//

import SwiftUI
import MapKit

extension CLLocationCoordinate2D {
    static let senioren1 = CLLocationCoordinate2D(latitude: 48.15310685057989, longitude: 48.15310685057989)
    static let senioren2 = CLLocationCoordinate2D(latitude: 48.2217739159893, longitude: 11.556700074826523)
    static let senioren3 = CLLocationCoordinate2D(latitude: 48.161500421754624, longitude: 11.540243000001539)
    static let senioren4 = CLLocationCoordinate2D(latitude: 48.182186423198345, longitude: 11.58426727116418)
    static let senioren5 = CLLocationCoordinate2D(latitude: 48.097115920868305, longitude: 11.649103271164108)
}

struct RouteView: View {
    @State private var route: MKRoute?
    @State private var travelTime: String?
    private let gradient = LinearGradient(colors: [.red, .orange], startPoint: .leading, endPoint: .trailing)
    private let stroke = StrokeStyle(lineWidth: 5, lineCap: .round, lineJoin: .round, dash: [8, 8])
    
    var body: some View {
        Map {
            if let route {
                MapPolyline(route.polyline)
                    .stroke(.blue, lineWidth: 8)
                    // .stroke(gradient, style: stroke)
            }
        }
        .overlay(alignment: .bottom, content: {
            HStack {
                if let travelTime {
                    Text("Travel time: \(travelTime)")
                        .padding()
                        .font(.headline)
                        .foregroundStyle(.black)
                        .background(.ultraThinMaterial)
                        .cornerRadius(15)
                }
            }
        })
        .onAppear(perform: {
            fetchRouteFrom(.senioren1, to: .senioren2)
        })
    }
}

extension RouteView {
    
    private func fetchRouteFrom(_ source: CLLocationCoordinate2D, to destination: CLLocationCoordinate2D) {
        let request = MKDirections.Request()
        request.source = MKMapItem(placemark: MKPlacemark(coordinate: source))
        request.destination = MKMapItem(placemark: MKPlacemark(coordinate: destination))
        request.transportType = .automobile
        
        Task {
            let result = try? await MKDirections(request: request).calculate()
            route = result?.routes.first
            getTravelTime()
        }
    }
    
    private func getTravelTime() {
        guard let route else { return }
        let formatter = DateComponentsFormatter()
        formatter.unitsStyle = .abbreviated
        formatter.allowedUnits = [.hour, .minute]
        travelTime = formatter.string(from: route.expectedTravelTime)
    }
}

#Preview {
    RouteView()
}
