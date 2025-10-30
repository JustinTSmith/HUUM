import SwiftUI

struct ContentView: View {
    @EnvironmentObject private var viewModel: SaunaViewModel

    var body: some View {
        VStack(spacing: 12) {
            if let temperature = viewModel.currentTemperature {
                Text("\(temperature)°C")
                    .font(.system(size: 36, weight: .semibold))
            } else {
                Text("--°C")
                    .font(.system(size: 36, weight: .semibold))
                    .redacted(reason: viewModel.isLoading ? .placeholder : [])
            }

            Stepper(value: $viewModel.targetTemperature, in: 40...110, step: 5) {
                Text("Target: \(viewModel.targetTemperature)°C")
            }
            .disabled(viewModel.isLoading)

            Button(action: { Task { await viewModel.toggleSauna() } }) {
                Text(viewModel.isHeating ? "Turn Off" : "Turn On")
                    .frame(maxWidth: .infinity)
            }
            .buttonStyle(.borderedProminent)
            .tint(viewModel.isHeating ? .red : .green)
            .disabled(viewModel.isLoading)

            Button("Refresh") {
                Task { await viewModel.refreshStatus() }
            }
            .buttonStyle(.bordered)
            .disabled(viewModel.isLoading)
        }
        .padding()
        .overlay(alignment: .bottom) {
            if let error = viewModel.errorMessage {
                Text(error)
                    .font(.footnote)
                    .foregroundColor(.yellow)
                    .multilineTextAlignment(.center)
                    .padding(.top)
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(SaunaViewModel())
    }
}
