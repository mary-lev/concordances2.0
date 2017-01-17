<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
 <xsl:output method="text"/>
 <xsl:strip-space elements="*"/>

<xsl:template match="info">
<h1>      <xsl:value-of select="name" />       <xsl:text>&#160;</xsl:text>       <xsl:value-of select="author" /></h1>
      <xsl:text>&#xa;</xsl:text>
<h2>      <xsl:value-of select="title" /></h2>
 </xsl:template>

<xsl:template match="stanza[line]">
     <xsl:text>&#xa;</xsl:text>
       <xsl:apply-templates select="line"/>
 </xsl:template>

 <xsl:template match="line[word]">
     <xsl:text>&#xa;</xsl:text>
       <xsl:apply-templates select="word"/>
 </xsl:template>

<xsl:template match="word[.!=',']">
   <xsl:if test=".!='.' and .!='!' and not(position() = 1)">
         <xsl:text> </xsl:text>
   </xsl:if>
  <xsl:apply-templates/>


 </xsl:template>
</xsl:stylesheet>