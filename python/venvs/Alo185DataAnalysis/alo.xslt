<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
     xmlns:media="http://search.yahoo.com/mrss">

  <xsl:output indent="yes" omit-xml-declaration="no"
       media-type="application/xml" encoding="UTF-8" />

  <xsl:template match="/">
    <searchresult>
      <xsl:apply-templates select="/csv_data/row" />
    </searchresult>
  </xsl:template>

  <xsl:template match="row">
    <document>
      <title><xsl:value-of select="f2" /></title>
      <snippet>
        <xsl:value-of select="f10" />
      </snippet>
      <url><xsl:value-of select="f1" /></url>
      
    </document>
  </xsl:template>
</xsl:stylesheet>