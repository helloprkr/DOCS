<?xml version="1.0" encoding="UTF-8"?>
<xs:schema 
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    targetNamespace="http://example.com/knowledge"
    xmlns="http://example.com/knowledge"
    elementFormDefault="qualified">

    <!-- 
      The schema defines a recursive, metamorphic structure that supports
      multiple abstraction layers (fisheye concept) within each MetaLayer (iteration).
      Each MetaLayer can reference previous/future layers and multiple abstraction levels.
    -->

    <xs:element name="KnowledgeSystem">
      <xs:complexType>
        <xs:sequence>
          <xs:element name="SchemaMetadata" minOccurs="0">
            <xs:complexType>
              <xs:sequence>
                <xs:element name="Version" type="xs:string" minOccurs="0"/>
                <xs:element name="Description" type="xs:string" minOccurs="0"/>
                <xs:element name="Author" type="xs:string" minOccurs="0"/>
                <xs:element name="CreatedDate" type="xs:date" minOccurs="0"/>
              </xs:sequence>
            </xs:complexType>
          </xs:element>
          <xs:element name="MetaLayers" minOccurs="1" maxOccurs="1">
            <xs:complexType>
              <xs:sequence>
                <xs:element name="MetaLayer" maxOccurs="unbounded">
                  <xs:complexType>
                    <xs:sequence>
                      <xs:element name="Description" type="xs:string" minOccurs="0"/>
                      <xs:element name="SeedPhrase" type="xs:string" minOccurs="0"/>
                      <xs:element name="Abstractions" minOccurs="1">
                        <xs:complexType>
                          <xs:sequence>
                            <xs:element name="Abstraction" maxOccurs="unbounded">
                              <xs:complexType>
                                <xs:sequence>
                                  <xs:element name="Content" type="xs:string"/>
                                  <xs:element name="ContextualReferences" minOccurs="0" maxOccurs="1">
                                    <xs:complexType>
                                      <xs:sequence>
                                        <!-- Links to other abstractions in same layer (zoom in/out) -->
                                        <xs:element name="ZoomInRef" type="xs:string" minOccurs="0" maxOccurs="unbounded"/>
                                        <xs:element name="ZoomOutRef" type="xs:string" minOccurs="0" maxOccurs="unbounded"/>
                                        <!-- Links to related MetaLayers -->
                                        <xs:element name="PreviousIterationRef" type="xs:string" minOccurs="0"/>
                                        <xs:element name="NextIterationRef" type="xs:string" minOccurs="0"/>
                                      </xs:sequence>
                                    </xs:complexType>
                                  </xs:element>
                                </xs:sequence>
                                <xs:attribute name="level" type="xs:string" use="required"/>
                              </xs:complexType>
                            </xs:element>
                          </xs:sequence>
                        </xs:complexType>
                      </xs:element>
                      <!-- Links to structural evolution: each MetaLayer can reference its conceptual neighbors -->
                      <xs:element name="EvolutionLinks" minOccurs="0">
                        <xs:complexType>
                          <xs:sequence>
                            <xs:element name="PriorLayerRef" type="xs:string" minOccurs="0"/>
                            <xs:element name="NextLayerRef" type="xs:string" minOccurs="0"/>
                          </xs:sequence>
                        </xs:complexType>
                      </xs:element>
                    </xs:sequence>
                    <xs:attribute name="index" type="xs:string" use="required"/>
                    <xs:attribute name="role" type="xs:string" use="optional"/>
                  </xs:complexType>
                </xs:element>
              </xs:sequence>
            </xs:complexType>
          </xs:element>

          <!-- Optional semantic or contextual expansions -->
          <xs:element name="ConceptualGraph" minOccurs="0">
            <xs:complexType>
              <xs:sequence>
                <xs:element name="Concept" maxOccurs="unbounded" minOccurs="0">
                  <xs:complexType>
                    <xs:sequence>
                      <xs:element name="Name" type="xs:string"/>
                      <xs:element name="RelatedConcepts" minOccurs="0">
                        <xs:complexType>
                          <xs:sequence>
                            <xs:element name="Related" type="xs:string" maxOccurs="unbounded" minOccurs="0"/>
                          </xs:sequence>
                        </xs:complexType>
                      </xs:element>
                    </xs:sequence>
                    <xs:attribute name="id" type="xs:string" use="required"/>
                  </xs:complexType>
                </xs:element>
              </xs:sequence>
            </xs:complexType>
          </xs:element>

          <xs:element name="ResourceLinks" minOccurs="0">
            <xs:complexType>
              <xs:sequence>
                <xs:element name="Link" maxOccurs="unbounded" minOccurs="0">
                  <xs:complexType>
                    <xs:attribute name="url" type="xs:anyURI" use="required"/>
                    <xs:attribute name="description" type="xs:string" use="optional"/>
                  </xs:complexType>
                </xs:element>
              </xs:sequence>
            </xs:complexType>
          </xs:element>

        </xs:sequence>
      </xs:complexType>
    </xs:element>

</xs:schema>
