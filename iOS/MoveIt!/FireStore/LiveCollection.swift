//
//  LiveCollection.swift
//  MoveIt!
//
//  Created by Harish Yerra on 11/15/19.
//  Copyright © 2019 MoveIt. All rights reserved.
//

import Foundation
import FirebaseFirestore

/// Maintains a live connection to FireStore and updates items as needed.
class LiveCollection<T: DictionaryDecodable>: ObservableObject {
    /// The items in the collection.
    @Published var items: [T]
    /// The documents in the collection.
    private(set) var documents: [DocumentSnapshot] = []
    /// The query to execute to fetch the collection.
    let query: Query
    
    /// The listner that will monitor for changes in the database.
    private var listener: ListenerRegistration? {
        didSet {
            oldValue?.remove()
        }
    }
    
    /// Creates a new `LiveCollection` to monitor changes in the FirestoreDatabase for a specified collection.
    /// - Parameter query: The query used to fetch the collection.
    init(query: Query) {
        self.items = []
        self.query = query
        listen()
    }
    
    /// Finds the first index of the document that shares the same id.
    /// - Parameter document: The document to find the match of.
    func index(of document: DocumentSnapshot) -> Int? {
        return documents.firstIndex { $0.documentID == document.documentID }
    }
    
    /// Starts listening for changes.
    private func listen() {
        guard listener == nil else { return }
        listener = query.addSnapshotListener { [unowned self] querySnapshot, error in
            // TODO: Perform error handling.
            guard let snapshot = querySnapshot else { return }
            let models = snapshot.documents.map { document -> T in
                var data = document.data()
                data["id"] = document.documentID
                guard let model = T(dictionary: data) else { fatalError("Unable to initialize type \(T.self) with dictionary \(data)") }
                return model
            }
            self.items = models
            self.documents = snapshot.documents
        }
    }
    
    deinit {
        listener = nil
    }
}
