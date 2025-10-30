import SwiftUI

@main
struct HuumSaunaWatchApp: App {
    @StateObject private var viewModel = SaunaViewModel()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(viewModel)
        }
    }
}
